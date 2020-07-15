import requests
import json
import pathlib
import re
import os

root = pathlib.Path(__file__).parent.resolve()


# TOKEN = os.environ.get("SIMONW_TOKEN", "")
limit = 5

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


def fetch_spotify(oauth_token):
    print("-----------------------")
    ret = []
    endpoint_url = "https://api.spotify.com/v1/me/top/tracks?"
    query = f'{endpoint_url}limit={limit}&time_range=short_term'

    response = requests.get(query,
                headers={"Content-Type": "application/json",
                            "Authorization": "Bearer BQB4Gr0hxRclX9Jbjj0HEbairCxEqr7F7KEMHgLH3aDyd6_MmCQqqOkNnTcg_MmsRgDd9sfAAQT5EUz3v2LAbzMzlVXC4UFIBvQBIOSHAhRTdsianzhOuU1_mlRa2QaPueS9YfgFeB9J02Xi2s0VkzH6RkEwIBHlxttITdEpbxSoQyZzydf86eiY82D76kvp-_ceOfQXlL-FX3AhCFL1Yybrq3-5ufJ4aIKLa_Y8xg70g-d_5pV4AfReRF6H4Led2OJV4VVTY4ne2M5QM6vJ"})
    json_response = response.json()
    uris = []
    # print(json_response)
    
    for i in json_response['items']:
            uris.append(i)
            print(f"\"{i['name']}\" by {i['artists'][0]['name']}")
            print(i['album']['images'][len(i['album']['images'])-1]['url'])
            ret.append("<tr> <td> <img src=\""+ i['album']['images'][len(i['album']['images'])-1]['url'] + "\"> </td> <td> <b>\"" + i['name'] + "\"</b> by " + i['artists'][0]['name']+ "</td> </tr>")
    print("-----------------------")
    
    return ret



if __name__ == "__main__":
    readme = root / "README.md"
    project_releases = root / "releases.md"
    res = fetch_spotify("EN")
    # print(res.json())
    # releases.sort(key=lambda r: r["published_at"], reverse=True)
    
    md = "\n".join(
        [
            song
            for song in res
        ]
    )
    print(md)
    readme_contents = readme.open().read()
    rewritten = replace_chunk(readme_contents, "top_tracks", md)
    readme.open("w").write(rewritten)
    
