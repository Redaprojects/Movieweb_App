# Tests route status and templates:

def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"MovieWeb" in response.data

def test_users_route(client):
    response = client.get('/users')
    assert response.status_code == 200

def test_404(client):
    response = client.get('/nonexistent')
    assert response.status_code == 404
