import io

import pytest
from PIL import Image

from app import create_app


@pytest.fixture
def client(tmp_path):
    """Configure an isolated Flask test client per test run."""
    app = create_app('testing')

    upload_dir = tmp_path / 'uploads'
    processed_dir = tmp_path / 'processed'
    rejected_dir = tmp_path / 'rejected'
    for directory in (upload_dir, processed_dir, rejected_dir):
        directory.mkdir(parents=True, exist_ok=True)

    app.config.update({
        'UPLOAD_FOLDER': str(upload_dir),
        'PROCESSED_FOLDER': str(processed_dir),
        'REJECTED_FOLDER': str(rejected_dir),
    })

    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    payload = response.get_json()
    assert payload['success'] is True
    assert payload['data']['status'] == 'healthy'


def test_validate_endpoint_without_file(client):
    response = client.post('/api/validate')
    assert response.status_code == 400
    payload = response.get_json()
    assert payload['success'] is False
    assert 'No image file provided' in payload['message']


def test_validate_endpoint_with_generated_image(client):
    image = Image.new('RGB', (1024, 768), color=(180, 180, 180))
    buffer = io.BytesIO()
    image.save(buffer, format='JPEG')
    buffer.seek(0)

    response = client.post(
        '/api/validate',
        data={'image': (buffer, 'sample.jpg')},
        content_type='multipart/form-data'
    )

    # Validation may return 200 for pass/fail; ensure we get a structured payload.
    assert response.status_code == 200
    payload = response.get_json()
    assert payload['success'] is True
    assert 'summary' in payload['data']
    assert 'checks' in payload['data']