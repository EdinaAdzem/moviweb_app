import pytest
from flask.testing import FlaskClient
from app import create_app
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



@pytest.fixture
def client() -> FlaskClient:
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_page(client):
    response = client.get('/')
    assert b"Welcome to MovieWeb" in response.data


def test_add_movie(client):
    response = client.post('/users/1/add_movie', data={
        'title': 'Inception',
        'rating': '8.8'
    })
    assert response.status_code == 302


def test_update_movie(client):
    response = client.post('/users/1/update_movie/1', data={'title': 'Updated Movie', 'director': 'Some Director', 'year': '2023', 'rating': '8.0'})
    assert response.status_code == 302


def test_delete_movie(client):
    response = client.post('/users/1/delete_movie/1')
    assert response.status_code == 302


def test_user_movies_not_found(client):
    response = client.get('/users/999/movies')
    assert response.status_code == 404


def test_form_validation(client):
    response = client.post('/users/1/add_movie', data={})
    assert response.status_code == 400
