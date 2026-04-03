import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import CacheFileHandler
from lingua import Language, LanguageDetectorBuilder

# 1. Absolute paths for safety
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# 2. Force a completely new cache file using the dedicated CacheFileHandler
CACHE_PATH = os.path.join(BASE_DIR, ".spotify_cache")
cache_handler = CacheFileHandler(cache_path=CACHE_PATH)

mcp = FastMCP("Spotify Assistant")

# 3. Updated auth manager with user-read-private and show_dialog=True
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-read-private user-library-read playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public",
    cache_handler=cache_handler,
    show_dialog=True
))

detector = LanguageDetectorBuilder.from_all_languages().with_low_accuracy_mode().build()

@mcp.tool()
def list_my_playlists():
    """Returns the names and IDs of the user's playlists."""
    results = sp.current_user_playlists()
    return [{"name": p['name'], "id": p['id']} for p in results['items']]

@mcp.tool()
def get_playlist_tracks(playlist_id: str):
    """Retrieves track details from a specific playlist (Handles massive 50+ hour playlists)."""
    tracks = []
    offset = 0
    limit = 50  # Strict maximum for the modern API
    
    while True:
        # Bypass spotipy's wrapper to force the modern /items endpoint directly
        results = sp._get(
            f"playlists/{playlist_id}/items", 
            limit=limit, 
            offset=offset, 
            market="IL"
        )
        
        for item in results.get('items', []):
            if item.get('item'):
                tracks.append({
                    "name": item['item']['name'],
                    "artist": item['item']['artists'][0]['name'],
                    "uri": item['item']['uri'],
                    "id": item['item']['id']
                })
        
        # Pagination to grab all songs (loops chunks of 50 until finished)
        if results.get('next'):
            offset += limit
        else:
            break
            
    return tracks

@mcp.tool()
def filter_tracks_by_language(tracks: list, target_language: str):
    """Filters a list of tracks by language using the song title."""
    filtered_uris = []
    for track in tracks:
        lang = detector.detect_language_of(track['name'])
        if lang and lang.name.lower() == target_language.lower():
            filtered_uris.append(track['uri'])
    return filtered_uris

@mcp.tool()
def create_playlist(name: str, track_uris: list):
    """Creates a new playlist and adds the provided tracks. (Cannot delete playlists)."""
    user_id = sp.current_user()['id']
    new_playlist = sp.user_playlist_create(user_id, name)
    
    # Spotify allows adding a maximum of 100 tracks per request, loop handles the rest
    for i in range(0, len(track_uris), 100):
        batch = track_uris[i:i+100]
        sp.playlist_add_items(new_playlist['id'], batch)
        
    return f"Success! Created '{name}' and added {len(track_uris)} tracks."

if __name__ == "__main__":
    mcp.run()