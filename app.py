# -*- coding: utf-8 -*-


from flask import Flask, render_template
from db import orm

app = Flask(__name__)
app.config.from_object('service.config')
orm.init_app(app)


@app.route('/')
def hello_world():
    return render_template("docs.html")

# from db_generator import create_all


# @app.route("/generate_all")
# def generate_all():
#     create_all()
#     return "DONE"


from views import phone_data_service_blueprint

app.register_blueprint(phone_data_service_blueprint, url_prefix='/phone_data_service')

if __name__ == '__main__':
    app.run(debug=True)
