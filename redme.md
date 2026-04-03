# Claude Spotify Assistant (MCP)

A Model Context Protocol (MCP) server that empowers Claude Desktop to securely manage, analyze, and organize your Spotify library. 

**Design Philosophy:** This tool is designed with a strict "Read/Create" architecture. It cannot delete playlists, remove saved tracks, or unfollow artists. Your library is safe.

## Features
* **Library Exploration:** Allow Claude to view your playlists and fetch track lists.
* **Deep Language Filtering:** Quickly parse massive playlists (e.g., 50+ hours) and isolate tracks by language using local NLP detection.
* **DJ & Set Preparation:** Extract audio features like BPM (Tempo), Energy, and Danceability to automatically sort tracks for mixing workflows.
* **Automated Playlist Creation:** Seamlessly generate new sub-playlists directly from chat prompts.

## Setup Instructions

### 1. Spotify Developer Credentials
1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).
2. Create an App.
3. Set the Redirect URI exactly to: `http://127.0.0.1:8888/callback`
4. Copy your **Client ID** and **Client Secret**.

### 2. Installation
Clone this repository and install the required packages:
```bash
pip install -r requirements.txt