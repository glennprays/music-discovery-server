from ytmusicapi import YTMusic

ytmusic = YTMusic("./gcp/oauth.json")

def search_music (query):
    search_results = ytmusic.search(query=query, filter='songs')
    return search_results