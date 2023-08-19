# Back-end Flask Restful API

## API Endpoints
### Autocomplete da Cidade
Method: GET

Endpoint: autocomplete_city

Parameters:
* user_input (required: True, String)

Example: https://climatempo-talent.rj.r.appspot.com/autocomplete_city?user_input=Osas

### Previsão do Tempo
Method: GET

Endpoint: weatherforecast

Parameters:
* city_id (required: True, Integer)
* unit_temperature (required: True, String, 'fahrenheit' ou 'celsius')
* unit_precipitation (required: True, String, 'inch' ou 'mm')

Example: https://climatempo-talent.rj.r.appspot.com/weatherforecast?city_id=3735&unit_temperature=fahrenheit&unit_precipitation=inch

## To Do
* Documentação da API (Swagger?)
* Remover caratéres especiais no autocomplete
