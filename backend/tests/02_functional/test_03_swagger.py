def test_swagger(app, client):
    res = client.get('/')
    assert res.status_code == 200
    data = res.get_data(as_text=True)
    assert '<!DOCTYPE html>' in data
    assert 'swagger' in data
