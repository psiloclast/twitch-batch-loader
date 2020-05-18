import re
import sys
import urllib

import requests


def get_clip(slug, client_id):
    return requests.get(
        f"https://api.twitch.tv/kraken/clips/{slug}",
        headers={"Accept": "application/vnd.twitchtv.v5+json", "Client-ID": client_id,},
    ).json()


def dl_progress(count, block_size, total_size):
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write("\r...%d%%" % percent)
    sys.stdout.flush()


client_id = sys.argv[1]
bad_chars = re.compile("[^a-zA-Z0-9_]")
download_path = "downloads/"

for slug in open("clips.txt", "r"):
    slug = slug.strip()
    clip = get_clip(slug, client_id)
    mp4_url = clip["thumbnails"]["medium"].replace("-preview-480x272.jpg", ".mp4")
    title = clip["title"]
    out_filename = bad_chars.sub("", title).replace(" ", "_") + ".mp4"
    output_path = download_path + out_filename

    print(f"Downloading clip: {slug}")
    print(f'"{title}" -> {out_filename}')
    print(mp4_url)

    urllib.request.urlretrieve(mp4_url, output_path, reporthook=dl_progress)

    print("\nDone.\n")

print("Finished downloading all the videos.")
