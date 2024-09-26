from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import manager as mg

SPOTIPY_ID = mg.SPOTIPY_ID
SPOTIPY_SECRET_KEY = mg.SPOTIPY_SECRET_KEY
SPOTIPY_REDIRECT_URL = "http://example.com"
USER_id = mg.USER_id


# spotify = SpotifyOAuth(client_id=SPOTIPY_ID, client_secret=SPOTIPY_SECRET_KEY, redirect_uri=SPOTIPY_REDIRECT_URL)
body = {
    "name": "Top-100",
    "description": "goat",
    "public": False
}

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=SPOTIPY_ID,
        client_secret=SPOTIPY_SECRET_KEY,
        show_dialog=True,
        cache_path="token.txt",
        username=USER_id,
    )
)
user_id = sp.current_user()["id"]
# response = requests.post(url=SPOTIFY_API_ENDPOINT, json=body)
# response.raise_for_status()
# print(response.text)
# print(response.status_code)


date = input("Which year dou you want to travel to? Type the date in this format YYYY-MM-DD: ")
URL = f"https://www.billboard.com/charts/hot-100/{date}"

response = requests.get(URL)
top_music = response.text

soup = BeautifulSoup(top_music, "html.parser")

title = soup.select(selector=".lrv-u-width-100p ul li #title-of-a-story")

song_names = [song.getText().strip() for song in title]
#
# print(song_list)

song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")


# SPOTIFY_API_ENDPOINT = f"https://api.spotify.com/v1/users/{user_id}/playlists"
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
# print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
