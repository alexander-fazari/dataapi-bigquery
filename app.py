import os
import pymysql
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from pybigquery import *

app = Flask(__name__)

# BIGQUERY
project_id = 'YOUR_GCP_PROJECTTID'
dataset_name = 'YOUR_BQ_DATASET'
credentials = 'credentials/my_key.json'
url = 'bigquery://'+project_id+"/"+dataset_name+"?credentials_path="+credentials

app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Covid(db.Model):
    '''
    @TODO
    '''
    date = db.Column(db.Date, primary_key=True)
    day = db.Column(db.Integer, unique=False)
    month = db.Column(db.Integer, unique=False)
    year = db.Column(db.Integer, unique=False)
    daily_confirmed_cases = db.Column(db.Integer, unique=False)
    daily_deaths = db.Column(db.Integer, unique=False)
    confirmed_cases = db.Column(db.Integer, unique=False)
    deaths = db.Column(db.Integer, unique=False)
    countries_and_territories = db.Column(db.String(300), primary_key=True)
    geo_id = db.Column(db.String(200), unique=False)
    country_territory_code = db.Column(db.String(200), unique=False)
    pop_data_2018 = db.Column(db.Integer, unique=False)


    def __init__(self, date, day, month, year, daily_confirmed_cases, daily_deaths, confirmed_cases, deaths,countries_and_territories, geo_id, country_territory_code, pop_data_2018):
        '''
        @TODO
        '''
        self.date = date
        self.day = day
        self.month = month
        self.year = year
        self.daily_confirmed_cases = daily_confirmed_cases
        self.daily_deaths = daily_deaths
        self.confirmed_cases = confirmed_cases
        self.deaths = deaths
        self.countries_and_territories = countries_and_territories
        self.geo_id = geo_id
        self.country_territory_code = country_territory_code
        self.pop_data_2018 = pop_data_2018

class CovidSchema(ma.Schema):
    class Meta:
        fields = ('date', 'day', 'month', 'year', 'daily_confirmed_cases', 'daily_deaths', 'confirmed_cases', 'deaths', 'countries_and_territories', 'geo_id', 'country_territory_code', 'pop_data_2018')

country_schema = CovidSchema()
countries_schema = CovidSchema(many=True)

# Return data all
@app.route("/countries", methods=["GET"])
def get_countries():
    all_countries = Covid.query.all()
    result = countries_schema.dump(all_countries)
    return jsonify(result)

# Return data by date
@app.route("/day/<date_id>", methods=["GET"])
def get_day(date_id):
    all_countries_day = Covid.query.filter_by(date=date_id)
    result = countries_schema.dump(all_countries_day)
    return jsonify(result)

# Return data by country geo_id
@app.route("/country/<geo>", methods=["GET"])
def country_detail(geo):
    country = Covid.query.filter_by(geo_id=geo)
    result = countries_schema.dump(country)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0',
            port=int(os.environ.get(
                     'PORT', 8080)))
