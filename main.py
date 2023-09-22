import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: \n")
URL = f"https://www.billboard.com/charts/hot-100/{date}/"
CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET")
USERNAME = os.environ.get("SPOTIPY_USERNAME")
REDIRECT_URI = os.environ.get("SPOTIPY_REDIRECT_URI")


response = requests.get(URL)
web_page = response.text

soup = BeautifulSoup(web_page, "html.parser")
song_titles = soup.select("li #title-of-a-story")

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=REDIRECT_URI,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
        username=USERNAME
    )
)

user_id = sp.current_user()["id"]
top_100_song = [name.getText().strip() for name in song_titles]

song_uris = []
year = date.split("-")[0]
for song in top_100_song:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# Creating a new private playlist in Spotify
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

# Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)


