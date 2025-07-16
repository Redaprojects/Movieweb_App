# Tests form submissions:

def test_add_user(client):
    response = client.post('/add_user', data={'name': 'TestUser'}, follow_redirects=True)
    assert b"TestUser" in response.data

def test_add_movie(client):
    # Add user first
    client.post('/add_user', data={'name': 'MovieOwner'})
    user_resp = client.get('/users')
    assert b"MovieOwner" in user_resp.data

    # Extract user ID
    from Movie_Web_App.datamanager.models import User
    user = User.query.filter_by(name='MovieOwner').first()

    response = client.post(f'/users/{user.id}/add_movie', data={
        'name': 'Inception',
        'director': 'Nolan',
        'year': '2010',
        'rating': '9.0'
    }, follow_redirects=True)

    assert b"Inception" in response.data
