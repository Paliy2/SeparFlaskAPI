# -*- coding: utf-8 -*-


from marshmallow import fields
from db import orm, ma


class AddUdpdateDelete():
    def add(self, resource):
        orm.session.add(resource)
        return orm.session.commit()

    def update(self):
        return orm.session.commit()

    def delete(self, resource):
        orm.session.delete(resource)
        return orm.session.commit()


class PhoneData(orm.Model, AddUdpdateDelete):
    __tablename__ = 'phone_data'
    id = orm.Column(orm.Integer, primary_key=True)
    address_city = orm.Column(orm.TEXT(), default='')
    address_street = orm.Column(orm.TEXT(), default='')
    address_house = orm.Column(orm.TEXT(), default='')
    address_entrance = orm.Column(orm.TEXT(), default='')
    location_latitude = orm.Column(orm.TEXT(), default='')
    location_longitude = orm.Column(orm.TEXT(), default='')
    first_name = orm.Column(orm.TEXT(), default='')
    phone_number = orm.Column(orm.TEXT(), default='')
    app = orm.Column(orm.TEXT(), default='')
    sent_times = orm.Column(orm.INT(), default=0)

    def __init__(self, phone_number,
                 address_city='',
                 address_street='',
                 address_house='',
                 address_entrance='',
                 location_latitude='',
                 location_longitude='',
                 first_name='',
                 app=''):
        self.address_city = address_city
        self.address_street = address_street
        self.address_house = address_house
        self.address_entrance = address_entrance
        self.location_latitude = location_latitude
        self.location_longitude = location_longitude
        self.first_name = first_name
        self.phone_number = phone_number
        self.app = app

    def __repr__(self):
        return '<Data id {}. Number {} Sent times: {}>'.format(self.id,
                                                               self.phone_number,
                                                               self.sent_times)

    def get_id(self):
        return str(self.id)


class PhoneDataSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    address_city = fields.Str()
    address_street = fields.Str()
    address_house = fields.Str()
    address_entrance = fields.Str()
    address_latitude = fields.Str()
    address_longitude = fields.Str()
    first_name = fields.Str()
    phone_number = fields.Str(required=True)
    app = fields.Str()
    sent_times = fields.Int()

    url = ma.URLFor('phone_data_service.phonedataresource', id='<id>', _external=True)
