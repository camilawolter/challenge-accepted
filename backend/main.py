import re

from flask import Flask, jsonify, request, abort
from flask_restful import Resource, Api

from marshmallow import Schema, fields, validate

import json

# General thoughts:
# Depending on the size of the locales.js file size, it may be worth loading it only once and keep it in memory during runtime.
# For the forecast.js file it is likely worth scheduling a reload with, for instance, apscheduler in order to retrieve up-to-date forecast data at all times.
# For this example usecase we will load the locales.js and forecast.js from disk every time an API call makes it necessary. This may be slow if a lot of API calls are issued. We recommend to "cache" the data in memory at least for 20 minutes or so.

# Here we create the flask app
app = Flask(__name__)
api = Api(app)

# Argument parsing
# The autocomplete_city endpoint allows for and requires only one argument: The user input string
class AutocompleteCityQuerySchema(Schema):
    user_input = fields.String(required=True)

# The weatherforecast endpoint requires as input the city_id (obtained through the autocomplete_city endpoint), the desired unit for .
class WeatherForecastQuerySchema(Schema):
    city_id = fields.Int(required=True)
    unit_temperature = fields.String(required=True, validate=validate.OneOf(["celsius", "fahrenheit"]))
    unit_precipitation = fields.String(required=True, validate=validate.OneOf(["mm", "inch"]))

autocompletecity_schema = AutocompleteCityQuerySchema()
weatherforecast_schema = WeatherForecastQuerySchema()

def FahrenheitFromCelsius(temperature_celsius):
    if isinstance(temperature_celsius, str):
        temperature_celsius = float(temperature_celsius)
    temperature_fahrenheit = 1.8 * temperature_celsius + 32.
    return round(temperature_fahrenheit)

def InchFromMillimeters(precipitation_millimeters):
    if isinstance(precipitation_millimeters, str):
        precipitation_millimeters = float(precipitation_millimeters)
    return round(precipitation_millimeters/25.4,1)

def nested_replace(structure, func, target_set_parent_key: set, target_set_key: set, parent_key=None, key=None):
    if type(structure) == list:
        return [nested_replace(item, func, target_set_parent_key, target_set_key, parent_key, key) for item in structure]

    if type(structure) == dict:
        return {child_key : nested_replace(child_value, func, target_set_parent_key, target_set_key, key, child_key) for child_key, child_value in structure.items() }

    if parent_key in target_set_parent_key and key in target_set_key:
        return func(structure)
    else:
        return structure

class AutocompleteCity(Resource):
    def get(self):
        # Validate parameters
        errors = autocompletecity_schema.validate(request.args)
        if errors:
            abort(400, str(errors))
        user_input_incomplete_city_name = request.args.get('user_input')
        output = {}
        with open('base/locales.json', 'r') as city_options_file:
            city_options_json = json.load(city_options_file)
            filtered = [{'id': city['id'], 'name': city['name'], 'state': city['state']} for city in city_options_json if user_input_incomplete_city_name in city['name']]
        output['results'] = filtered
        return jsonify(output)

class WeatherForecast(Resource):
    def get(self):
        # Validate parameters
        errors = weatherforecast_schema.validate(request.args)
        if errors:
            abort(400, str(errors))
        city_id = int(request.args.get('city_id'))
        unit_temperature = request.args.get('unit_temperature')
        unit_precipitation = request.args.get('unit_precipitation')
        filtered = None
        output = {}
        with open('base/weather.json', 'r') as forecast_file:
            forecast_json = json.load(forecast_file)
            # If unit Fahrenheit is requested, substitute all temperature values according to the conversion formula
            if unit_temperature == "fahrenheit":
                forecast_json = nested_replace(forecast_json, FahrenheitFromCelsius, {"temperature"}, {"min", "max"})
            if unit_precipitation == "inch":
                forecast_json = nested_replace(forecast_json, InchFromMillimeters, {"rain"}, {"precipitation"})
            filtered = [forecast for forecast in forecast_json if city_id == forecast['locale']['id']]
        if filtered:
            return jsonify(filtered)
        output['error'] = f'No weather forecast was found for your city. Please contact our support team and inform the requested city_id: {city_id}.'
        output['city_id'] = city_id
        return jsonify(output)
    
api.add_resource(AutocompleteCity, '/autocomplete_city')
api.add_resource(WeatherForecast, '/weatherforecast')

if __name__ == '__main__':
    #app.run(debug=True)
    app.run()

