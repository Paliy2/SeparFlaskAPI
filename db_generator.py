from glob import glob
from models import PhoneData


# YOu dont need that piece of code- I already uploaded it to the db.
def read_add_fdata_to_db(f_name):
    with open(f_name, 'r', encoding='utf-8') as f:
        all_rows = [r.split(",") for r in f.read().split("\n")[1:-1]]

    for data in all_rows:
        phone_data = PhoneData(phone_number=data[-2],
                               address_city=data[0],
                               address_street=data[1],
                               address_house=data[2],
                               address_entrance=data[3],
                               location_latitude=data[4],
                               location_longitude=data[5],
                               first_name=data[6],
                               app=data[-1]
                               )
        phone_data.add(phone_data)
        print(phone_data)


def create_all():
    # function is called form endpoint in the app.py
    path = "path_to_part3_file (can be relative)/"
    for f_name in glob(path + "*.csv"):
        res = read_add_fdata_to_db(f_name)
