import json

def test_weatherforecast_without_arguments(app, client):
    res = client.get('/weatherforecast')
    assert res.status_code == 400
    data = json.loads(res.get_data(as_text=True))
    assert 'errors' in data
    assert isinstance(data['errors'], dict)
    assert 'city_id' in data['errors']
    assert isinstance(data['errors']['city_id'], str)
    assert 'Número identificador do local. Missing required parameter' in data['errors']['city_id']

def test_weatherforecast_with_empty_city_id(app, client):
    res = client.get('/weatherforecast?city_id=')
    assert res.status_code == 400
    data = json.loads(res.get_data(as_text=True))
    assert 'errors' in data
    assert isinstance(data['errors'], dict)
    assert 'city_id' in data['errors']
    assert isinstance(data['errors']['city_id'], str)
    assert 'Número identificador do local. invalid literal for int()' in data['errors']['city_id']

def test_weatherforecast_with_null_city_id_without_unit_temperature(app, client):
    res = client.get('/weatherforecast?city_id=0')
    assert res.status_code == 400
    data = json.loads(res.get_data(as_text=True))
    assert 'errors' in data
    assert isinstance(data['errors'], dict)
    assert 'unit_temperature' in data['errors']
    assert isinstance(data['errors']['unit_temperature'], str)
    assert 'Missing required parameter' in data['errors']['unit_temperature']

def test_weatherforecast_with_null_city_id_with_empty_unit_temperature(app, client):
    res = client.get('/weatherforecast?city_id=0&unit_temperature=')
    assert res.status_code == 400
    data = json.loads(res.get_data(as_text=True))
    assert 'errors' in data
    assert isinstance(data['errors'], dict)
    assert 'unit_precipitation' in data['errors']
    assert isinstance(data['errors']['unit_precipitation'], str)
    assert 'Unidade de precipitação: "mm" ou "inch". Missing required parameter' in data['errors']['unit_precipitation']

def test_weatherforecast_with_null_city_id_with_empty_unit_temperature_with_empty_unit_precipitation(app, client):
    res = client.get('/weatherforecast?city_id=0&unit_temperature=&unit_precipitation=')
    assert res.status_code == 400
    data = res.get_data(as_text=True)
    assert 'Wrong unit for temperature: . Must be one of "celsius" and "fahrenheit".' in data

def test_weatherforecast_with_null_city_id_with_celsius_as_unit_temperature_with_empty_unit_precipitation(app, client):
    res = client.get('/weatherforecast?city_id=0&unit_temperature=celsius&unit_precipitation=')
    assert res.status_code == 400
    data = res.get_data(as_text=True)
    assert 'Wrong unit for precipitation: . Must be one of "mm" and "inch".' in data

def test_weatherforecast_with_null_city_id_with_fahrenheit_as_unit_temperature_with_empty_unit_precipitation(app, client):
    res = client.get('/weatherforecast?city_id=0&unit_temperature=fahrenheit&unit_precipitation=')
    assert res.status_code == 400
    data = res.get_data(as_text=True)
    assert 'Wrong unit for precipitation: . Must be one of "mm" and "inch".' in data

def test_weatherforecast_with_null_city_id_with_celsius_as_unit_temperature_with_mm_as_unit_precipitation(app, client):
    res = client.get('/weatherforecast?city_id=0&unit_temperature=celsius&unit_precipitation=mm')
    assert res.status_code == 400
    data = res.get_data(as_text=True)
    assert 'No weather forecast was found for your city.' in data

def test_weatherforecast_with_Sao_Paulo_city_id_with_celsius_as_unit_temperature_with_mm_as_unit_precipitation(app, client):
    res = client.get('/weatherforecast?city_id=3477&unit_temperature=celsius&unit_precipitation=mm')
    assert res.status_code == 200
    data = json.loads(res.get_data(as_text=True))
    expected_object = [{"locale":{"id":3477,"latitude":-23.548,"longitude":-46.636,"name":"São Paulo","state":"SP"},"period":{"begin":"2017-02-01","end":"2017-02-07"},"weather":[{"date":"2017-02-01","rain":{"precipitation":20,"probability":60},"temperature":{"max":27,"min":19},"text":"Sol com muitas nuvens durante o dia. Per\u00edodos de nublado, com chuva a qualquer hora."},{"date":"2017-02-02","rain":{"precipitation":15,"probability":60},"temperature":{"max":29,"min":20},"text":"Sol com muitas nuvens durante o dia. Per\u00edodos de nublado, com chuva a qualquer hora."},{"date":"2017-02-03","rain":{"precipitation":15,"probability":60},"temperature":{"max":30,"min":21},"text":"Sol com algumas nuvens. Chove r\u00e1pido durante o dia e \u00e0 noite."},{"date":"2017-02-04","rain":{"precipitation":11,"probability":60},"temperature":{"max":31,"min":21},"text":"Sol com algumas nuvens. Chove r\u00e1pido durante o dia e \u00e0 noite."},{"date":"2017-02-05","rain":{"precipitation":16,"probability":67},"temperature":{"max":31,"min":22},"text":"Sol e aumento de nuvens de manh\u00e3. Pancadas de chuva \u00e0 tarde e \u00e0 noite."},{"date":"2017-02-06","rain":{"precipitation":"8","probability":60},"temperature":{"max":32,"min":21},"text":"Sol com algumas nuvens. Chove r\u00e1pido durante o dia e \u00e0 noite."},{"date":"2017-02-07","rain":{"precipitation":26,"probability":60},"temperature":{"max":33,"min":22},"text":"Sol com algumas nuvens. Chove r\u00e1pido durante o dia e \u00e0 noite."}]}]
    assert expected_object == data

def test_weatherforecast_with_Sao_Paulo_city_id_with_fahrenheit_as_unit_temperature_with_mm_as_unit_precipitation(app, client):
    res = client.get('/weatherforecast?city_id=3477&unit_temperature=fahrenheit&unit_precipitation=mm')
    assert res.status_code == 200
    data = json.loads(res.get_data(as_text=True))
    expected_object = [{"locale":{"id":3477,"latitude":-23.548,"longitude":-46.636,"name":"S\u00e3o Paulo","state":"SP"},"period":{"begin":"2017-02-01","end":"2017-02-07"},"weather":[{"date":"2017-02-01","rain":{"precipitation":20,"probability":60},"temperature":{"max":81,"min":66},"text":"Sol com muitas nuvens durante o dia. Per\u00edodos de nublado, com chuva a qualquer hora."},{"date":"2017-02-02","rain":{"precipitation":15,"probability":60},"temperature":{"max":84,"min":68},"text":"Sol com muitas nuvens durante o dia. Per\u00edodos de nublado, com chuva a qualquer hora."},{"date":"2017-02-03","rain":{"precipitation":15,"probability":60},"temperature":{"max":86,"min":70},"text":"Sol com algumas nuvens. Chove r\u00e1pido durante o dia e \u00e0 noite."},{"date":"2017-02-04","rain":{"precipitation":11,"probability":60},"temperature":{"max":88,"min":70},"text":"Sol com algumas nuvens. Chove r\u00e1pido durante o dia e \u00e0 noite."},{"date":"2017-02-05","rain":{"precipitation":16,"probability":67},"temperature":{"max":88,"min":72},"text":"Sol e aumento de nuvens de manh\u00e3. Pancadas de chuva \u00e0 tarde e \u00e0 noite."},{"date":"2017-02-06","rain":{"precipitation":"8","probability":60},"temperature":{"max":90,"min":70},"text":"Sol com algumas nuvens. Chove r\u00e1pido durante o dia e \u00e0 noite."},{"date":"2017-02-07","rain":{"precipitation":26,"probability":60},"temperature":{"max":91,"min":72},"text":"Sol com algumas nuvens. Chove r\u00e1pido durante o dia e \u00e0 noite."}]}]
    assert expected_object == data

def test_weatherforecast_with_Sao_Paulo_city_id_with_celsius_as_unit_temperature_with_inch_as_unit_precipitation(app, client):
    res = client.get('/weatherforecast?city_id=3477&unit_temperature=celsius&unit_precipitation=inch')
    assert res.status_code == 200
    data = json.loads(res.get_data(as_text=True))
    expected_object = [{"locale":{"id":3477,"latitude":-23.548,"longitude":-46.636,"name":"S\u00e3o Paulo","state":"SP"},"period":{"begin":"2017-02-01","end":"2017-02-07"},"weather":[{"date":"2017-02-01","rain":{"precipitation":0.8,"probability":60},"temperature":{"max":27,"min":19},"text":"Sol com muitas nuvens durante o dia. Per\u00edodos de nublado, com chuva a qualquer hora."},{"date":"2017-02-02","rain":{"precipitation":0.6,"probability":60},"temperature":{"max":29,"min":20},"text":"Sol com muitas nuvens durante o dia. Per\u00edodos de nublado, com chuva a qualquer hora."},{"date":"2017-02-03","rain":{"precipitation":0.6,"probability":60},"temperature":{"max":30,"min":21},"text":"Sol com algumas nuvens. Chove r\u00e1pido durante o dia e \u00e0 noite."},{"date":"2017-02-04","rain":{"precipitation":0.4,"probability":60},"temperature":{"max":31,"min":21},"text":"Sol com algumas nuvens. Chove r\u00e1pido durante o dia e \u00e0 noite."},{"date":"2017-02-05","rain":{"precipitation":0.6,"probability":67},"temperature":{"max":31,"min":22},"text":"Sol e aumento de nuvens de manh\u00e3. Pancadas de chuva \u00e0 tarde e \u00e0 noite."},{"date":"2017-02-06","rain":{"precipitation":0.3,"probability":60},"temperature":{"max":32,"min":21},"text":"Sol com algumas nuvens. Chove r\u00e1pido durante o dia e \u00e0 noite."},{"date":"2017-02-07","rain":{"precipitation":1.0,"probability":60},"temperature":{"max":33,"min":22},"text":"Sol com algumas nuvens. Chove r\u00e1pido durante o dia e \u00e0 noite."}]}]
    assert expected_object == data

def test_weatherforecast_with_Sao_Paulo_city_id_with_fahrenheit_as_unit_temperature_with_inch_as_unit_precipitation(app, client):
    res = client.get('/weatherforecast?city_id=3477&unit_temperature=fahrenheit&unit_precipitation=inch')
    assert res.status_code == 200
    data = json.loads(res.get_data(as_text=True))
    expected_object = [{"locale":{"id":3477,"latitude":-23.548,"longitude":-46.636,"name":"S\u00e3o Paulo","state":"SP"},"period":{"begin":"2017-02-01","end":"2017-02-07"},"weather":[{"date":"2017-02-01","rain":{"precipitation":0.8,"probability":60},"temperature":{"max":81,"min":66},"text":"Sol com muitas nuvens durante o dia. Per\u00edodos de nublado, com chuva a qualquer hora."},{"date":"2017-02-02","rain":{"precipitation":0.6,"probability":60},"temperature":{"max":84,"min":68},"text":"Sol com muitas nuvens durante o dia. Per\u00edodos de nublado, com chuva a qualquer hora."},{"date":"2017-02-03","rain":{"precipitation":0.6,"probability":60},"temperature":{"max":86,"min":70},"text":"Sol com algumas nuvens. Chove r\u00e1pido durante o dia e \u00e0 noite."},{"date":"2017-02-04","rain":{"precipitation":0.4,"probability":60},"temperature":{"max":88,"min":70},"text":"Sol com algumas nuvens. Chove r\u00e1pido durante o dia e \u00e0 noite."},{"date":"2017-02-05","rain":{"precipitation":0.6,"probability":67},"temperature":{"max":88,"min":72},"text":"Sol e aumento de nuvens de manh\u00e3. Pancadas de chuva \u00e0 tarde e \u00e0 noite."},{"date":"2017-02-06","rain":{"precipitation":0.3,"probability":60},"temperature":{"max":90,"min":70},"text":"Sol com algumas nuvens. Chove r\u00e1pido durante o dia e \u00e0 noite."},{"date":"2017-02-07","rain":{"precipitation":1.0,"probability":60},"temperature":{"max":91,"min":72},"text":"Sol com algumas nuvens. Chove r\u00e1pido durante o dia e \u00e0 noite."}]}]
    assert expected_object == data

