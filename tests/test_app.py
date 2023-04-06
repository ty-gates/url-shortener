import pytest
from myapp.app import app, db, URL


# Test the index route
def test_index():
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        assert b'URL Shortener' in response.data

# Test the shorten route
def test_shorten():
    with app.test_client() as client:
        response = client.post('/shorten', data={'url': 'http://example.com'})
        assert response.status_code == 200
        assert b'Your shortened URL is:' in response.data

        # Check that a URL object was added to the database
        url = URL.query.filter_by(long_url='http://example.com').first()
        assert url is not None

# Test the redirect route
def test_redirect():
    with app.test_client() as client:
        # First create a URL object in the database
        url = URL(long_url='http://example.com', short_url='abcd1234')
        db.session.add(url)
        db.session.commit()

        # Now try to redirect to that URL
        response = client.get('/abcd1234')
        assert response.status_code == 302
        assert response.location == 'http://example.com'

# Test that a non-existent short URL returns an error message
def test_invalid_short_url():
    with app.test_client() as client:
        response = client.get('/nonexistent')
        assert response.status_code == 200
        assert b'Invalid URL' in response.data
