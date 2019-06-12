"""
    get_allimages_by_name.py
    MediaWiki Action API Code Samples
    List all images in the namespace, starting from files that
    begin with 'Graffiti_000'. Limit the initial response to
    just the first three images.
    MIT License
"""
import json
import sys

import requests

S = requests.Session()

URL = "https://commons.wikimedia.org/w/api.php"

PARAMS = {
    "action": "query",
    "generator": "categorymembers",
    "gcmtitle": "Category:Featured pictures on Wikimedia Commons",
    "gcmlimit": "50",
    "gcmtype": "file",
    "prop": "imageinfo",
    "iiprop": "url|size|mime",
    "iiurlwidth": "1024",
    "format": "json"
}

gallery = []

left = True
page = 1
while left:
    print(page, file=sys.stderr)
    page += 1

    r = S.get(url=URL, params=PARAMS)
    data = r.json()

    for _, p in data["query"]["pages"].items():
        image_info = p["imageinfo"][0]

        if not image_info["mime"].startswith("image"):
            continue

        if image_info["mime"] == "image/gif":
            continue

        gallery.append({
            "src": image_info["thumburl"],
            "width": image_info["thumbwidth"],
            "height": image_info["thumbheight"]
        })

    if "continue" in data:
        PARAMS["continue"] = data["continue"]["continue"]
        PARAMS["gcmcontinue"] = data["continue"]["gcmcontinue"]
    else:
        left = False

print(json.dumps(gallery))
