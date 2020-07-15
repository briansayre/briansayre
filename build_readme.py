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
                            "Authorization": "Bearer BQBh--_VkZlE-5-ar1WmoUeLFaENACjm4r2K8LpUEcY_RGXQnxoyWROuiY3lL3MTE-bDbYpb0yNGyIeQCphWCFh8fgaZ9i7XdiMCVFIvWjl-KDmBN0i5nW7a5t0aThe5v_HL62kWxHTAr8IQJkh8QtPSUbfzhq02WTXs3ZNAg0Xrdf849RRPUossQ-LK5n05Ly8Z55I8Bjr1XkR3yncYki_BYwaPhn7X0zqR1Vn8e0tAj3VaFWG5dWPSMG_prOkicVyjw9vb2mxAv2y7TyqH"})
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
    
