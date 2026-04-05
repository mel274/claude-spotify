# Claude Spotify Assistant (MCP)

A Model Context Protocol (MCP) server that empowers Claude Desktop to securely manage, analyze, and organize your Spotify library.

**Design Philosophy:** This tool is designed with a strict "Read/Create" architecture. It cannot delete playlists, remove saved tracks, or unfollow artists. Your library is safe.

## Features
* **Library Exploration:** Allow Claude to view your playlists and fetch track lists.
* **Deep Language Filtering:** Quickly parse massive playlists (e.g., 50+ hours) and isolate tracks by language using local NLP detection (`lingua-language-detector`).
* **DJ & Set Preparation:** Extract audio features like BPM (Tempo), Energy, and Danceability to automatically sort tracks for mixing workflows.
* **Automated Playlist Creation:** Seamlessly generate new sub-playlists directly from chat prompts, with automatic batch handling for large track lists.

## Setup Instructions

### 1. Spotify Developer Credentials
1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).
2. Create an App.
3. Set the Redirect URI exactly to: `http://127.0.0.1:8888/callback`.
4. Copy your **Client ID** and **Client Secret**.

### 2. Environment Configuration
Create a `.env` file in the root directory of the project. You can use `.env.exemple` as a template:

```env
SPOTIPY_CLIENT_ID=your_actual_client_id
SPOTIPY_CLIENT_SECRET=your_actual_client_secret
SPOTIPY_REDIRECT_URI=[http://127.0.0.1:8888/callback](http://127.0.0.1:8888/callback)
```

### 3. Installation
Clone this repository and install the required packages:
```bash
pip install -r requirements.txt
```

## Claude Desktop Configuration

To integrate this server with Claude Desktop, add the following to your `claude_desktop_config.json`. This setup points to your local Python installation and the `server.py` file, which will automatically load your credentials from the `.env` file.

**File Location:**
* **macOS:** `~/Library/Application Support/Anthropic/claude_desktop_config.json`
* **Windows:** `%APPDATA%\Anthropic\claude_desktop_config.json`

**Configuration:**
```json
{
  "mcpServers": {
    "spotify-assistant": {
      "command": "python",
      "args": [
        "/absolute/path/to/your/project/server.py"
      ]
    }
  }
}
```
*Replace `/absolute/path/to/your/project/server.py` with the actual full path on your machine.*

## Available Tools
* `list_my_playlists`: Returns the names and IDs of the user's playlists.
* `get_playlist_tracks`: Retrieves track details from a specific playlist (handles pagination for large lists).
* `filter_tracks_by_language`: Filters a list of tracks by language using the song title.
* `create_playlist`: Creates a new playlist and adds the provided tracks in batches.
```
