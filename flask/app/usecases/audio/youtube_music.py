from ytmusicapi import YTMusic
import os

# current_dir = os.path.dirname(os.path.abspath(__file__))
# oauth_json_path = os.path.join(current_dir, "../../../gcp/oauth.json")

ytmusic = YTMusic("./gcp/oauth.json")
# ytmusic = YTMusic(oauth_json_path)

def search_music (query):
    search_results = ytmusic.search(query=query, filter='songs')
    return search_results