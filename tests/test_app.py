import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    # Arrange: No special setup needed as activities are predefined

    # Act: Make GET request to /activities
    response = client.get("/activities")

    # Assert: Check status code and response content
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_success():
    # Arrange: Choose an activity and email not already signed up
    activity_name = "Basketball Team"
    email = "newstudent@mergington.edu"

    # Act: Make POST request to signup
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert: Check success response
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert f"Signed up {email} for {activity_name}" in data["message"]


def test_signup_activity_not_found():
    # Arrange: Use a non-existent activity name
    activity_name = "NonExistent Activity"
    email = "student@mergington.edu"

    # Act: Make POST request to signup
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert: Check 404 error
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_signup_already_signed_up():
    # Arrange: Use an activity and email that's already signed up
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already in participants

    # Act: Make POST request to signup
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert: Check 400 error
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Student already signed up for this activity" in data["detail"]


def test_unregister_success():
    # Arrange: First sign up, then unregister
    activity_name = "Tennis Club"
    email = "teststudent@mergington.edu"

    # Sign up first
    signup_response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert signup_response.status_code == 200

    # Act: Make DELETE request to unregister
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert: Check success response
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert f"Unregistered {email} from {activity_name}" in data["message"]


def test_unregister_activity_not_found():
    # Arrange: Use a non-existent activity name
    activity_name = "NonExistent Activity"
    email = "student@mergington.edu"

    # Act: Make DELETE request to unregister
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert: Check 404 error
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_unregister_not_signed_up():
    # Arrange: Use an activity and email that's not signed up
    activity_name = "Art Studio"
    email = "notsignedup@mergington.edu"

    # Act: Make DELETE request to unregister
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert: Check 400 error
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Student not signed up for this activity" in data["detail"]