import requests
import json
import pathlib
import re
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

root = pathlib.Path(__file__).parent.resolve()

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
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, username="thebriansayre"))
    results = sp.current_user_top_tracks(limit=3, offset=0, time_range='short_term')
    for item in results['items']:
        song_title = item['name']
        img_url = item['album']['images'][len(item['album']['images'])-1]['url']
        artist = item['artists'][0]['name']
        tracks.append("<tr> <td> <img src=\""+ img_url + "\"> </td> <td> <b>\"" + song_title + "\"</b> by " + artist + "</td> </tr>")
    return tracks


if __name__ == "__main__":
    readme = root / "README.md"
    tracks = fetch_spotify_top_tracks()
    md = "\n".join(
        [
            track
            for track in tracks
        ]
    )
    print(md)
    readme_contents = readme.open().read()
    rewritten = replace_chunk(readme_contents, "top_tracks", md)
    readme.open("w").write(rewritten)
    
