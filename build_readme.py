import re
import os

import pathlib
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import (datetime, timedelta)

root = pathlib.Path(__file__).parent.resolve()
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')


def replace_chunk(content, marker, chunk, inline=False):
    r = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    if not inline:
        chunk = "\n{}\n".format(chunk)
    chunk = "<!-- {} starts -->{}<!-- {} ends -->".format(
        marker, chunk, marker)
    return r.sub(chunk, content)


def fetch_spotify_top_tracks():
    tracks = []
    scope = "user-top-read"
    username="thebriansayre"
    auth_manager = SpotifyOAuth(
        scope=scope,
        username=username,
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)
    results = sp.current_user_top_tracks(limit=5, offset=0, time_range='short_term')
    for item in results['items']:
        song_title = item['name']
        img_url = item['album']['images'][len(item['album']['images'])-1]['url']
        artist = item['artists'][0]['name']
        preview_url = item['preview_url']
        if not preview_url:
            preview_url = "https://github.com/briansayre" 
        tracks.append("    <tr>")
        tracks.append("        <td> <img height=\"32px\" src=\""+ img_url + "\"> </td>")
        tracks.append("        <td> <b>\"" + song_title + "\"</b> by " + artist + "</td>")
        tracks.append("        <td> <a href=\"" + preview_url + "\" target=\"_blank\" > Preview </a> </td>")
        tracks.append("    </tr>")
        print(song_title)
    return tracks

    
def fetch_spotify_top_artists():
    artists = []
    scope = "user-top-read"
    username="thebriansayre"
    auth_manager = SpotifyOAuth(
        scope=scope,
        username=username,
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)
    results = sp.current_user_top_artists(limit=5, offset=0, time_range='medium_term')
    print(results)
    for item in results['items']:
        artist_name = item['name']
        img_url = item['images'][len(item['images'])-1]['url']
        preview_url = item['external_urls']["spotify"]
        if len(item["genres"]) != 0: 
            genre = item["genres"][len(item["genres"])-1]
        else:
            genre = "no genre"
        if not preview_url:
            preview_url = "https://github.com/briansayre" 
        artists.append("    <tr>")
        artists.append("        <td> <img height=\"32px\" src=\""+ img_url + "\"> </td>")
        artists.append("        <td> <b>" + artist_name + "</b></td>")
        artists.append("        <td> <i>" + genre + "</i></td>")
        artists.append("        <td> <a href=\"" + preview_url + "\" target=\"_blank\" > Preview </a> </td>")
        artists.append("    </tr>")
        print(artist_name)
    return artists


if __name__ == "__main__":
    # Update Spotify artists
    readme = root / "README.md"
    artists = fetch_spotify_top_artists()
    
    md = "\n".join(
        [
            artist
            for artist in artists
        ]
    )
    readme_contents = readme.open().read()
    rewritten = replace_chunk(readme_contents, "top_artists", md)

    # Update the last updated time
    now = datetime.now()
    nowCST = now - timedelta(hours=5)
    dt_string = nowCST.strftime("%m/%d/%Y at %H:%M:%S")
    last_updated = ("> Artists last updated on " + dt_string + " CST")
    rewritten = replace_chunk(rewritten, "last_updated", last_updated)
    # Write to README
    readme.open("w").write(rewritten)
