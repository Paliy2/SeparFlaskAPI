# -*- coding: utf-8 -*-


from flask import Blueprint, request, jsonify, make_response
from flask_restful import Resource, Api
from pytz import unicode
from sqlalchemy import desc

from service.http_status import HttpStatus
from db import orm
from models import PhoneData, PhoneDataSchema
from sqlalchemy.exc import SQLAlchemyError
from service.helpers import PaginationHelper
from marshmallow import Schema, fields, EXCLUDE, INCLUDE, RAISE

phone_data_service_blueprint = Blueprint('phone_data_service', __name__)
phone_data_schema = PhoneDataSchema(unknown=INCLUDE)
service = Api(phone_data_service_blueprint)


class PhoneDataResource(Resource):
    def get(self, id):
        phone_data = PhoneData.query.get_or_404(id)
        dump_result = phone_data_schema.dump(phone_data)
        return dump_result

    def patch(self, id):
        phone_data = PhoneData.query.get_or_404(id)
        phone_data_dict = request.get_json(force=True)
        for col_name in ['sent_times', 'phone_number', 'address_city',
                         'address_street', 'address_house',
                         'address_entrance', 'location_latitude',
                         'location_longitude', 'first_name', 'app']:
            if col_name in phone_data_dict and phone_data_dict[col_name] is not None:
                phone_data.col_name = phone_data_dict[col_name]

        dumped_phone_data = phone_data_schema.dump(phone_data)
        validate_errors = phone_data_schema.validate(dumped_phone_data)
        if validate_errors:
            return validate_errors, HttpStatus.bad_request_400.value
        try:
            phone_data.update()
            return self.get(id)
        except SQLAlchemyError as e:
            orm.session.rollback()
            response = {"error": str(e)}
            return response, HttpStatus.bad_request_400.value

    def delete(self, id):
        phone_data = PhoneData.query.get_or_404(id)
        try:
            delete = phone_data.delete(phone_data)
            response = make_response()
            return response, HttpStatus.no_content_204.value
        except SQLAlchemyError as e:
            orm.session.rollback()
            response = {"error": str(e)}
            return response, HttpStatus.unauthorized_401.value


class PhoneDataIncrementStatisticsResource(Resource):
    def get(self, id):
        phone_data = PhoneData.query.get_or_404(id)
        if phone_data:
            phone_data.sent_times += 1
        phone_data.update()
        dump_result = phone_data_schema.dump(phone_data)
        return dump_result


class PhoneDataListResource(Resource):
    def get(self):
        pagination_helper = PaginationHelper(
            request,
            query=PhoneData.query,
            resource_for_url='phone_data_service.phonedatalistresource',
            key_name='results',
            schema=phone_data_schema)
        pagination_result = pagination_helper.paginate_query()
        return pagination_result

    def post(self):
        phone_data_dict = request.get_json()

        if not phone_data_dict:
            response = {'message': 'No input data provided'}
            return response, HttpStatus.bad_request_400.value
        errors = phone_data_schema.validate(phone_data_dict)
        if errors:
            return errors, HttpStatus.bad_request_400.value
        for col_name in ['address_city',
                         'address_street', 'address_house',
                         'address_entrance', 'location_latitude',
                         'location_longitude', 'first_name', 'app']:
            if col_name not in phone_data_dict.keys():
                phone_data_dict[col_name] = ''
        try:
            phone_data = PhoneData(
                phone_number=phone_data_dict['phone_number'],
                address_city=phone_data_dict['address_city'],
                address_street=phone_data_dict['address_street'],
                address_house=phone_data_dict['address_house'],
                address_entrance=phone_data_dict['address_entrance'],
                location_latitude=phone_data_dict['location_latitude'],
                location_longitude=phone_data_dict['location_longitude'],
                first_name=phone_data_dict['first_name'],
                app=phone_data_dict['app'])
            phone_data.add(phone_data)
            query = PhoneData.query.get(phone_data.id)
            return phone_data_schema.dump(query), HttpStatus.created_201.value
        except SQLAlchemyError as e:
            orm.session.rollback()
            response = {"error": str(e)}
            return response, HttpStatus.bad_request_400.value


class NotSendDataListResource(Resource):
    def get(self):
        pagination_helper = PaginationHelper(
            request,
            query=PhoneData.query.filter(PhoneData.sent_times == 0),
            resource_for_url='phone_data_service.notsenddatalistresource',
            key_name='results',
            schema=phone_data_schema)
        pagination_result = pagination_helper.paginate_query()
        return pagination_result


class TopSendPhones(Resource):
    def get(self):
        pagination_helper = PaginationHelper(
            request,
            query=PhoneData.query.filter(PhoneData.sent_times != 0
                                         ).order_by(desc(PhoneData.sent_times)),
            resource_for_url='phone_data_service.notsenddatalistresource',
            key_name='results',
            schema=phone_data_schema)
        pagination_result = pagination_helper.paginate_query()
        return pagination_result


service.add_resource(PhoneDataListResource, '/phone_data/')
service.add_resource(NotSendDataListResource, '/not_sent_phone_data/')
service.add_resource(TopSendPhones, '/top_down_sent_phone_data/')
service.add_resource(PhoneDataResource, '/phone_data/<int:id>')
service.add_resource(PhoneDataIncrementStatisticsResource, '/increment_sent_statistics/<int:id>')
