import requests
import json
import pathlib
import re
import os

root = pathlib.Path(__file__).parent.resolve()


# TOKEN = os.environ.get("SIMONW_TOKEN", "")
limit = 3

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
                            "Authorization": "Bearer BQA2UKNlYtinhusPBDKHEbHWX4HIIVQqN0EA9iZ2btSOI3-7ETbtCCXpk6pZYF-3KMRdaR_7t9PzEKp5ohrPP6u2vznMGqH-zM5eO9gz9uqDPzYsEVm0qeWonD6VOB4u4a7AyEj6KWeYFvI3EXaW1d4aWwqpbzf8WQruM1L7pov9jrjRTpwQkFu4yO2uN1yp5eurVbveKmQATb1D7EPqxMcZ1YWB-Vdy3q2Lymvy7aWj3Ii27yRWnNSJTgnVTz-6OMqo3DiOOatEbauekMIQ"})
    json_response = response.json()
    uris = []
    # print(json_response)
    
    for i in json_response['items']:
            uris.append(i)
            print(f"\"{i['name']}\" by {i['artists'][0]['name']}")
            ret.append("\"" + i['name'] + "\" by " + i['artists'][0]['name'])
    print("-----------------------")
    
    return ret



if __name__ == "__main__":
    readme = root / "README.md"
    project_releases = root / "releases.md"
    res = fetch_spotify(TOKEN)
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
    
