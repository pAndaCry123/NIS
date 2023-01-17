import datetime

import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Float, DateTime,Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import enum

db_string = "postgresql://postgres:test@localhost:5432/postgres"
db = create_engine(db_string)
base = declarative_base()

Session = sessionmaker(db)
session = Session()

class Weather(base):
    __tablename__ = 'weather_nis'

    id = Column(Integer, primary_key=True)
    time_stamp = Column(DateTime)
    temperature = Column(Float)
    wind_gust = Column(Float)
    wind_speed = Column(Float)
    solar_radiation = Column(Float)
    load = Column(Float)


    def __init__(self, **kwargs):

        self.time_stamp = datetime.datetime.strptime(str(kwargs['datetime']),'%Y-%m-%dT%H:%M:%S')
        self.temperature =round(float(kwargs['temp']), 2)
        self.humidity = round(float(kwargs['humidity']), 2)
        self.wind_gust = round(float(kwargs['windgust']), 2)
        self.wind_speed = round(float(kwargs['windspeed']), 2)
        self.solar_radiation = round(float(kwargs['solarradiation']), 2)
        self.load = round(float(kwargs['load']), 2)

def impute(df, col_name):
    import numpy as np
    for ind in df.index:
        if np.isnan(df[col_name][ind]):
            temp = df[col_name].iloc[ind - 15:ind + 15].dropna()
            df[col_name][ind] = temp.mean()

def return_all_elements():
    weathers = session.query(Weather).all()
    return weathers


def read_from_csv():
    data_frame =  pd.read_csv('test_data.csv')
    data =  pd.read_csv('predicted_values.csv')
    for index, row in data_frame.iterrows():
        # logic to change conditions where is null
        row_dict = row.to_dict()

        if np.isnan(row_dict['solarradiation']):
            row_dict['solarradiation'] = 0
        row_dict['load'] = data['load'][index]
        weather = Weather(**row_dict)
        store_to_database(weather)

def store_to_database(model):
    session.add(model)
    session.commit()


if __name__ == "__main__":
    base.metadata.create_all(db)