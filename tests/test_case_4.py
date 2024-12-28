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


def test_edit_user_data_conflict(api_client):
    """
    Test that editing user data fails if the data is already taken.
    """
    # Step 1: Fetch the list of users
    users_endpoint = f"{BASE_URL}users/"
    response = api_client.get(users_endpoint)
    assert response.status_code == 200, f"Expected 200, but got {response.status_code}"

    users = response.json()
    assert isinstance(users, list), "Expected the response to be a list of users."
    assert len(users) > 1, "At least two users are required for this test."

    # Step 2: Pick two users for testing
    user_1, user_2 = random.sample(users, 2)
    user_1_uuid = user_1["uuid"]
    user_2_email = user_2["email"]
    user_2_nick = user_2["nickname"]

    # Step 3: Prepare payload using user_2's email or nickname
    conflict_payload_email = {"email": user_2_email}
    conflict_payload_nick = {"nickname": user_2_nick}

    # Step 4: Attempt to update user_1 with user_2's email
    edit_user_endpoint = f"{BASE_URL}users/{user_1_uuid}/"
    response_email_conflict = api_client.patch(edit_user_endpoint, json=conflict_payload_email)
    assert response_email_conflict.status_code == 409, (
        f"Expected 409 Conflict, but got {response_email_conflict.status_code}"
    )

    # Assert the response contains the expected error message for email conflict
    conflict_email_message = response_email_conflict.json()
    assert "already taken" in conflict_email_message["message"], (
        f"Expected conflict message to contain 'already taken', but got: {conflict_email_message['message']}"
    )
    assert user_2_email in conflict_email_message["message"], (
        f"Expected conflict message to include the conflicting email: {user_2_email}"
    )

    # Step 5: Attempt to update user_1 with user_2's nickname
    response_nick_conflict = api_client.patch(edit_user_endpoint, json=conflict_payload_nick)
    assert response_nick_conflict.status_code == 409, (
        f"Expected 409 Conflict, but got {response_nick_conflict.status_code}"
    )

    # Assert the response contains the expected error message for nickname conflict
    conflict_nick_message = response_nick_conflict.json()
    assert "already taken" in conflict_nick_message["message"], (
        f"Expected conflict message to contain 'already taken', but got: {conflict_nick_message['message']}"
    )
    assert user_2_nick in conflict_nick_message["message"], (
        f"Expected conflict message to include the conflicting nickname: {user_2_nick}"
    )

    print("Conflict tests for editing user data passed successfully.")
