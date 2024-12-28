import pytest
import requests
import random

BASE_URL = "http://127.0.0.1:8000/api/v1/"
HEADERS = {"Authorization": "Bearer b27912f4-78fd-4d15-977c-1325d4b64732"}


@pytest.fixture(scope="module")
def api_client():
    session = requests.Session()
    session.headers.update(HEADERS)
    return session


def test_search_song_by_partial_name(api_client):
    songs_endpoint = f"{BASE_URL}songs/"
    response = api_client.get(songs_endpoint)
    assert response.status_code == 200, f"Expected 200, but got {response.status_code}"

    songs = response.json()
    assert isinstance(songs, list), "Expected the response to be a list of songs."
    assert len(songs) > 0, "The list of songs should not be empty."

    # Adjust for the correct key (e.g., 'title')
    for song in songs:
        assert "title" in song, f"'title' key is missing in song: {song}"

    random_song = random.choice(songs)
    song_name = random_song["title"]
    var_1 = song_name[:3]
    print(f"Randomly selected song: {song_name}, Partial search term: {var_1}")

    query_params = {"search": var_1}
    search_response = api_client.get(songs_endpoint, params=query_params)
    assert search_response.status_code == 200, f"Expected 200, but got {search_response.status_code}"

    matching_songs = [song for song in songs if var_1.lower() in song["title"].lower()]
    search_results = search_response.json()
    assert isinstance(search_results, list), "Expected search results to be a list."
    assert sorted(search_results, key=lambda x: x["title"]) == sorted(matching_songs, key=lambda x: x["title"]), (
        "Search results do not match the expected list of songs."
    )
    print("Search results are valid and match the expected data.")


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
#     session = requests.Session()
#     session.headers.update(HEADERS)
#     return session
#
#
# def test_search_song_by_partial_name(api_client):
#     songs_endpoint = f"{BASE_URL}songs/"
#     response = api_client.get(songs_endpoint)
#     assert response.status_code == 200, f"Expected 200, but got {response.status_code}"
#
#     songs = response.json()
#     print(songs)
#     assert isinstance(songs, list), "Expected the response to be a list of songs."
#     assert len(songs) > 0, "The list of songs should not be empty."