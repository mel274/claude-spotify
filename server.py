import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from lingua import Language, LanguageDetectorBuilder

# Load environment variables
load_dotenv()

# Initialize the MCP Server
mcp = FastMCP("Spotify Assistant")

# Initialize Spotify Client (Safe Scopes Only)
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-library-read playlist-read-private playlist-modify-private playlist-modify-public"
))

# Setup Language Detector
detector = LanguageDetectorBuilder.from_all_languages().with_low_accuracy_mode().build()

@mcp.tool()
def list_my_playlists():
    """Returns the names and IDs of the user's playlists."""
    results = sp.current_user_playlists()
    return [{"name": p['name'], "id": p['id']} for p in results['items']]

@mcp.tool()
def get_playlist_tracks(playlist_id: str):
    """Retrieves track details (name, artist, uri, id) from a specific playlist."""
    results = sp.playlist_items(playlist_id)
    tracks = []
    for item in results['items']:
        if item['track']:
            tracks.append({
                "name": item['track']['name'],
                "artist": item['track']['artists'][0]['name'],
                "uri": item['track']['uri'],
                "id": item['track']['id']
            })
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
def get_track_audio_features(track_ids: list):
    """Retrieves BPM (tempo), energy, and danceability for a list of track IDs."""
    # Spotify API limits audio features requests to 100 tracks at a time
    features = []
    for i in range(0, len(track_ids), 100):
        batch = track_ids[i:i+100]
        batch_features = sp.audio_features(batch)
        features.extend([f for f in batch_features if f is not None])
    
    return [{"id": f['id'], "tempo": f['tempo'], "energy": f['energy'], "danceability": f['danceability']} for f in features]

@mcp.tool()
def create_playlist(name: str, track_uris: list):
    """Creates a new playlist and adds the provided tracks. (Cannot delete playlists)."""
    user_id = sp.current_user()['id']
    new_playlist = sp.user_playlist_create(user_id, name)
    
    # Spotify allows adding a maximum of 100 tracks per request
    for i in range(0, len(track_uris), 100):
        batch = track_uris[i:i+100]
        sp.playlist_add_items(new_playlist['id'], batch)
        
    return f"Success! Created '{name}' and added {len(track_uris)} tracks."

if __name__ == "__main__":
    mcp.run()