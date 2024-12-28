# import pytest
# import requests
# import random
#
# BASE_URL = "http://127.0.0.1:8000/api/v1/"
# HEADERS = {"Authorization": "Bearer b27912f4-78fd-4d15-977c-1325d4b64732"}
#
#
# @pytest.fixture(scope="module")
# def api_client():
#     """
#     Provides a session object configured with default headers for API requests.
#     """
#     session = requests.Session()
#     session.headers.update(HEADERS)
#     return session
#
#
# def test_create_new_user(api_client):
#     """
#     Test creating a new user in the system.
#     """
#     # Step 1: Prepare the payload with valid data
#     email = f"user{random.randint(1, 1000)}@example.com"
#     payload = {
#         "email": email,
#         "password": "WAwawa1234$",
#         "name": "Test User",
#         "nickname": "testuser"
#     }
#
#     # Step 2: Send POST request to create a new user
#     create_user_endpoint = f"{BASE_URL}users/"
#     response = api_client.post(create_user_endpoint, json=payload)
#
#     # Step 3: Assert the response status is 200
#     assert response.status_code == 200, f"Expected 200, but got {response.status_code}. Response body: {response.text}"
#
#     # Step 4: Assert the response contains the correct format
#     user_data = response.json()
#     expected_keys = ["email", "name", "nickname", "avatar_url", "uuid"]  # Correct 'nickname' instead of 'nick'
#     for key in expected_keys:
#         assert key in user_data, f"Key '{key}' is missing in the response."
#
#     assert user_data["email"] == payload["email"], "Email does not match."
#     assert user_data["name"] == payload["name"], "Name does not match."
#     assert user_data["nickname"] == payload[
#         "nickname"], "Nickname does not match."  # Correct 'nickname' instead of 'nick'
#
#     # Adjust the check for avatar_url to handle both None and empty string
#     assert user_data["avatar_url"] is None or user_data["avatar_url"] == "", "Avatar URL should be empty or None."
#
#     assert isinstance(user_data["uuid"], str) and len(user_data["uuid"]) == 36, "Invalid UUID format."
#
#     # Step 5: Save the user's UUID for further validation
#     new_user_uuid = user_data["uuid"]
#
#     # Step 6: Verify the new user exists in the list of users
#     list_users_endpoint = f"{BASE_URL}users/"
#     list_response = api_client.get(list_users_endpoint)
#     assert list_response.status_code == 200, f"Expected 200, but got {list_response.status_code}"
#
#     users = list_response.json()
#     assert isinstance(users, list), "Expected the response to be a list of users."
#     assert any(user["uuid"] == new_user_uuid for user in users), "New user is not found in the list of users."
#
#     # Step 7: Validate that when searching for the new user by UUID, data is displayed correctly
#     user_details_endpoint = f"{BASE_URL}users/{new_user_uuid}/"
#     user_details_response = api_client.get(user_details_endpoint)
#     assert user_details_response.status_code == 200, f"Expected 200, but got {user_details_response.status_code}"
#
#     user_details = user_details_response.json()
#     assert user_details == user_data, "User details do not match the created user data."
#
#     print("User creation test passed successfully.")

import pytest
import requests
import random

BASE_URL = "http://127.0.0.1:8000/api/v1/"
HEADERS = {"Authorization": "Bearer b27912f4-78fd-4d15-977c-1325d4b64732"}


@pytest.fixture(scope="module")
def api_client():
    """
    Provides a session object configured with default headers for API requests.
    """
    session = requests.Session()
    session.headers.update(HEADERS)
    return session


def test_create_new_user(api_client):
    """
    Test creating a new user in the system.
    """
    # Step 1: Prepare the payload with valid data
    email = f"user{random.randint(1, 1000)}@example.com"
    payload = {
        "email": email,
        "password": "Fafa1234$",
        "name": "Test TUser",
        "nickname": "testtuser"
    }

    # Step 2: Send POST request to create a new user
    create_user_endpoint = f"{BASE_URL}users/"
    response = api_client.post(create_user_endpoint, json=payload)

    # Step 3: Assert the response status is 200
    assert response.status_code == 200, f"Expected 200, but got {response.status_code}. Response body: {response.text}"

    # Step 4: Assert the response contains the correct format
    user_data = response.json()
    expected_keys = ["email", "name", "nickname", "avatar_url", "uuid"]  # Correct 'nickname' instead of 'nick'
    for key in expected_keys:
        assert key in user_data, f"Key '{key}' is missing in the response."

    assert user_data["email"] == payload["email"], "Email does not match."
    assert user_data["name"] == payload["name"], "Name does not match."
    assert user_data["nickname"] == payload[
        "nickname"], "Nickname does not match."  # Correct 'nickname' instead of 'nick'

    # Adjust the check for avatar_url to handle both None and empty string
    assert user_data["avatar_url"] is None or user_data["avatar_url"] == "", "Avatar URL should be empty or None."

    assert isinstance(user_data["uuid"], str) and len(user_data["uuid"]) == 36, "Invalid UUID format."

    # Step 5: Verify the new user exists in the list of users
    list_users_endpoint = f"{BASE_URL}users/"
    list_response = api_client.get(list_users_endpoint)
    assert list_response.status_code == 200, f"Expected 200, but got {list_response.status_code}"

    users = list_response.json()
    assert isinstance(users, list), "Expected the response to be a list of users."
    assert any(user["uuid"] == user_data["uuid"] for user in users), "New user is not found in the list of users."

    # Step 6: Validate that when searching for the new user by UUID, data is displayed correctly
    user_details_endpoint = f"{BASE_URL}users/{user_data['uuid']}/"
    user_details_response = api_client.get(user_details_endpoint)
    assert user_details_response.status_code == 200, f"Expected 200, but got {user_details_response.status_code}"

    user_details = user_details_response.json()
    assert user_details == user_data, "User details do not match the created user data."

    print("User creation test passed successfully.")
