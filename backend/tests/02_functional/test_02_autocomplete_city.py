import json

def test_autocomplete_city_without_arguments(app, client):
    res = client.get('/autocomplete_city')
    assert res.status_code == 400
    data = json.loads(res.get_data(as_text=True))
    assert 'errors' in data
    assert isinstance(data['errors'], dict)
    assert 'user_input' in data['errors']
    assert isinstance(data['errors']['user_input'], str)
    assert 'Nome incompleto da cidade digitado pelo usuário. Missing required parameter' in data['errors']['user_input']

def test_autocomplete_city_with_empty_user_input(app, client):
    res = client.get('/autocomplete_city?user_input=')
    assert res.status_code == 200
    data = json.loads(res.get_data(as_text=True))
    assert 'results' in data
    assert isinstance(data['results'],list)
    assert len(data['results']) > 0

def test_autocomplete_city_with_absurd_user_input(app, client):
    res = client.get('/autocomplete_city?user_input=XXXXXXXXXXXXXXXXXXXXXXXXXX')
    assert res.status_code == 200
    data = json.loads(res.get_data(as_text=True))
    assert 'results' in data
    assert isinstance(data['results'],list)
    assert len(data['results']) == 0

def test_autocomplete_city_with_correct_user_input_Sao_Paulo_tilde(app, client):
    res = client.get('/autocomplete_city?user_input=São Paulo')
    assert res.status_code == 200
    data = json.loads(res.get_data(as_text=True))
    assert 'results' in data
    assert isinstance(data['results'],list)
    assert len(data['results']) > 0
    expected_object = {"id": 3477, "name": "São Paulo", "state": "SP"}
    assert expected_object in data['results']

def test_autocomplete_city_with_correct_user_input_Sao_Paulo_notilde(app, client):
    res = client.get('/autocomplete_city?user_input=Sao Paulo')
    assert res.status_code == 200
    data = json.loads(res.get_data(as_text=True))
    assert 'results' in data
    assert isinstance(data['results'],list)
    assert len(data['results']) > 0
    expected_object = {"id": 3477, "name": "São Paulo", "state": "SP"}
    assert expected_object in data['results']

def test_autocomplete_city_with_correct_user_input_Sao_Paulo_CAPITAL(app, client):
    res = client.get('/autocomplete_city?user_input=SÃO PAULO')
    assert res.status_code == 200
    data = json.loads(res.get_data(as_text=True))
    assert 'results' in data
    assert isinstance(data['results'],list)
    assert len(data['results']) > 0
    expected_object = {"id": 3477, "name": "São Paulo", "state": "SP"}
    assert expected_object in data['results']

