import pytest
from flask import Flask
from app import app  # Import the Flask app

@pytest.fixture
def client():
    """Test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_check_quality_no_image(client):
    """Test check_quality endpoint with no image."""
    response = client.post('/check_quality')
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'No image uploaded'

def test_check_quality_with_image(client, sample_image):
    """Test check_quality endpoint with a sample image."""
    # This would need actual image data
    # For now, just test the structure
    pass