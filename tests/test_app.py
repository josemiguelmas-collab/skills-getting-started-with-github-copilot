import pytest
from fastapi.testclient import TestClient
from src.app import app, activities
import copy

@pytest.fixture(autouse=True)
def reset_activities():
    # Arrange: guardar y restaurar el estado original de activities
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(copy.deepcopy(original))

def test_get_activities():
    # Arrange
    client = TestClient(app)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_participant():
    client = TestClient(app)
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert email in activities[activity]["participants"]
    assert "Signed up" in response.json()["message"]

def test_signup_duplicate_participant():
    client = TestClient(app)
    activity = "Chess Club"
    email = activities[activity]["participants"][0]
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_remove_participant():
    client = TestClient(app)
    activity = "Chess Club"
    email = activities[activity]["participants"][0]
    # Act
    response = client.delete(f"/activities/{activity}/participants/{email}")
    # Assert
    assert response.status_code == 200
    assert email not in activities[activity]["participants"]
    assert "Removed" in response.json()["message"]

def test_remove_nonexistent_participant():
    client = TestClient(app)
    activity = "Chess Club"
    email = "notfound@mergington.edu"
    # Act
    response = client.delete(f"/activities/{activity}/participants/{email}")
    # Assert
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]

def test_signup_nonexistent_activity():
    client = TestClient(app)
    activity = "Nonexistent Club"
    email = "test@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
