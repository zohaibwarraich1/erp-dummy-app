import pytest
import os
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_hello_endpoint(client):
    # Set dummy environment variables to simulate Kubernetes injects
    os.environ['TENANT_NAME'] = 'Test Tenant'
    os.environ['DATABASE_HOST'] = 'test-db-svc'
    os.environ['DATABASE_NAME'] = 'erp_test'
    os.environ['POSTGRES_PASSWORD'] = 'test-secret-password'
    # Mocking the APP_ENV
    os.environ['APP_ENV'] = 'development'

    response = client.get('/')
    assert response.status_code == 200

    data = response.get_json()
    assert data["message"] == "Welcome to the ERP system for Test Tenant!"
    assert data["environment"] == "development"
    assert data["database"]["host"] == "test-db-svc"
    assert data["database"]["name"] == "erp_test"
    assert data["database"]["connection_status"] == "Connected"
