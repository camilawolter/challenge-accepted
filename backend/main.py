from flask import Flask, jsonify, request, abort, Response
from flask_restx import Api, Resource, reqparse
from flask_caching import Cache

import json

from unidecode import unidecode

# General thoughts:
# Depending on the size of the locales.js file size, it may be worth loading it only once and keep it in memory during runtime.
# For the forecast.js file it is likely worth scheduling a reload with, for instance, apscheduler in order to retrieve up-to-date forecast data at all times.
# For this example usecase we will load the locales.js and forecast.js from disk every time an API call makes it necessary. This may be slow if a lot of API calls are issued. We recommend to "cache" the data in memory at least for 20 minutes or so.

# Here we create the flask app
config = {
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 900
}
app = Flask(__name__)
app.config.SWAGGER_UI_DOC_EXPANSION = 'list'
api = Api(app, version="0.1", title="Climatempo Talent REST API", description="Essa API fornece endpoints para acessar a autocompletação de nomes de cidades e a previsão do tempo.")
cache = Cache(app, config=config)

# Argument parsing
# The autocomplete_city endpoint allows for and requires only one argument: The user input string
autocomplete_city_parser = reqparse.RequestParser()
autocomplete_city_parser.add_argument('user_input', required=True, type=str, help='Nome incompleto da cidade digitado pelo usuário.')
# The weatherforecast endpoint requires as input the city_id (obtained through the autocomplete_city endpoint) and the desired units for temperature and precipitation.
weatherforecast_parser = reqparse.RequestParser()
weatherforecast_parser.add_argument('city_id', required=True, type=int, help='Número identificador do local.')
weatherforecast_parser.add_argument('unit_temperature', required=True, type=str, help='Unidade de temperatura: "celsius" ou "fahrenheit".')
weatherforecast_parser.add_argument('unit_precipitation', required=True, type=str, help='Unidade de precipitação: "mm" ou "inch".')

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

    
@api.route('/autocomplete_city')
class AutocompleteCity(Resource):
    # Enable cache with 30 minutes timeout
    @api.expect(autocomplete_city_parser)
    @cache.cached(timeout=1800, query_string=True)
    def get(self):
        # Validate parameters
        args = autocomplete_city_parser.parse_args()
        user_input_incomplete_city_name = args['user_input']
        user_input_incomplete_city_name = unidecode(user_input_incomplete_city_name).lower()
        output = {}
        with open('base/locales.json', 'r') as city_options_file:
            city_options_json = json.load(city_options_file)
            filtered = [{'id': city['id'], 'name': city['name'], 'state': city['state']} for city in city_options_json if user_input_incomplete_city_name in unidecode(city['name']).lower()]
        output['results'] = filtered
        return jsonify(output)

@api.route('/weatherforecast')
class WeatherForecast(Resource):
    # Enable cache with 5 minutes timeout
    @api.expect(weatherforecast_parser)
    @cache.cached(timeout=300, query_string=True)
    def get(self):
        # Validate parameters
        args = weatherforecast_parser.parse_args()
        city_id = int(args['city_id'])
        unit_temperature = args['unit_temperature']
        unit_precipitation = args['unit_precipitation']
        filtered = None
        with open('base/weather.json', 'r') as forecast_file:
            forecast_json = json.load(forecast_file)
            # If unit Fahrenheit is requested, substitute all temperature values according to the conversion formula.
            if unit_temperature == "fahrenheit":
                forecast_json = nested_replace(forecast_json, FahrenheitFromCelsius, {"temperature"}, {"min", "max"})
            elif unit_temperature == "celsius":
                pass
            else:
                return Response(f'Wrong unit for temperature: {unit_temperature}. Must be one of "celsius" and "fahrenheit".', status=400)
            # If unit Inch is requested, substitute all precipitation values according to the conversion formula.
            if unit_precipitation == "inch":
                forecast_json = nested_replace(forecast_json, InchFromMillimeters, {"rain"}, {"precipitation"})
            elif unit_precipitation == "mm":
                pass
            else:
                return Response(f'Wrong unit for precipitation: {unit_precipitation}. Must be one of "mm" and "inch".', status=400)
            filtered = [forecast for forecast in forecast_json if city_id == forecast['locale']['id']]
        if filtered:
            return jsonify(filtered)
        return Response(f'No weather forecast was found for your city. Please contact our support team and inform the requested city_id: {city_id}.', status=400)

if __name__ == '__main__':
    app.run(debug=True)

