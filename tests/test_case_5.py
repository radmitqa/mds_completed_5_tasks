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


def test_update_wishlist(api_client):
    """
    Test updating the wishlist of a user by adding a song.
    """
    # Step 1: Fetch the list of users
    users_endpoint = f"{BASE_URL}users/"
    response_users = api_client.get(users_endpoint)
    assert response_users.status_code == 200, f"Expected 200, but got {response_users.status_code}"

    users = response_users.json()
    assert isinstance(users, list), "Expected the response to be a list of users."
    assert len(users) > 0, "No users found in the system."

    # Step 2: Pick a random user and collect their UUID
    random_user = random.choice(users)
    user_uuid = random_user["uuid"]

    # Step 3: Fetch the list of songs
    songs_endpoint = f"{BASE_URL}songs/"
    response_songs = api_client.get(songs_endpoint)
    assert response_songs.status_code == 200, f"Expected 200, but got {response_songs.status_code}"

    songs = response_songs.json()
    assert isinstance(songs, list), "Expected the response to be a list of songs."
    assert len(songs) > 0, "No songs found in the system."

    # Step 4: Pick a random song and collect its UUID
    random_song = random.choice(songs)
    song_uuid = random_song["uuid"]

    # Step 5: Prepare the payload
    payload = {"item_uuid": song_uuid}

    # Step 6: Send POST request to add the song to the user's wishlist
    add_to_wishlist_endpoint = f"{BASE_URL}users/{user_uuid}/wishlist/add/"
    response_add = api_client.post(add_to_wishlist_endpoint, json=payload)
    assert response_add.status_code == 200, f"Expected 200, but got {response_add.status_code}"

    # Step 7: Fetch the user's wishlist and verify the song was added
    wishlist_endpoint = f"{BASE_URL}users/{user_uuid}/wishlist/"
    response_wishlist = api_client.get(wishlist_endpoint)
    assert response_wishlist.status_code == 200, f"Expected 200, but got {response_wishlist.status_code}"

    wishlist = response_wishlist.json()
    assert "items" in wishlist, "The response does not contain the 'items' key."
    items = wishlist["items"]
    assert isinstance(items, list), "Expected 'items' to be a list."
    assert any(item["uuid"] == song_uuid for item in items), "The song was not added to the wishlist."

    print(f"User {user_uuid}'s wishlist updated successfully with song {song_uuid}.")
