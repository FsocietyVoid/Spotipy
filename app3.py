import csv
import os
from pathlib import Path
from flask import Flask, request, jsonify, render_template
from youtubesearchpython import VideosSearch
from yt_dlp import YoutubeDL
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Flask setup
app = Flask(__name__)

# Global variables for API credentials
SPOTIPY_CLIENT_ID = None
SPOTIPY_CLIENT_SECRET = None
SPOTIPY_REDIRECT_URI = None

# CSV and local path for songs
SONGS_TRACKER = "songs.csv"
DESKTOP_PATH = Path.home() / "Desktop" / "Songs"
DESKTOP_PATH.mkdir(parents=True, exist_ok=True)  # Ensure folder exists

# Functions to handle song tracking and downloading
def getDownloadedSongs():
    """Get the list of songs already downloaded."""
    if not os.path.exists(SONGS_TRACKER):
        return []
    downloaded_songs = []
    with open(SONGS_TRACKER, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            if len(row) < 2:
                continue  # Skip rows that don't have both song name and artist
            song_name = row[0].strip()
            artist_name = row[1].strip()
            downloaded_songs.append(f"{song_name} by {artist_name}")
    return downloaded_songs

def getNewSong(song, artist):
    """Track the downloaded song by adding it to the CSV file."""
    with open(SONGS_TRACKER, 'a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([song, artist])

def downloadSong(song, artist):
    """Download the song from YouTube based on the Spotify metadata."""
    song_query = f"{song} by {artist}"
    search = VideosSearch(song_query, limit=1)
    result = search.result()['result'][0]
    youtube_url = result['link']
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': str(DESKTOP_PATH / f"{song_query}.%(ext)s"),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

@app.route('/')
def index():
    """Render the homepage with a form to input Spotify credentials."""
    return render_template('index.html')

@app.route('/set_credentials', methods=['POST'])
def set_credentials():
    """Set Spotify API credentials manually."""
    global SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI
    SPOTIPY_CLIENT_ID = request.form['client_id']
    SPOTIPY_CLIENT_SECRET = request.form['client_secret']
    SPOTIPY_REDIRECT_URI = request.form['redirect_uri']
    return jsonify({'message': 'Spotify credentials set successfully!'}), 200

@app.route('/list_songs', methods=['POST'])
def list_songs():
    """List songs from the provided Spotify playlist link."""
    if not (SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET and SPOTIPY_REDIRECT_URI):
        return jsonify({'error': 'Spotify API credentials not set!'}), 400

    try:
        playlist_url = request.form['playlist_url']
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                                       client_secret=SPOTIPY_CLIENT_SECRET,
                                                       redirect_uri=SPOTIPY_REDIRECT_URI,
                                                       scope="playlist-read-private"))

        playlist_id = playlist_url.split("/")[-1].split("?")[0]
        playlist = sp.playlist(playlist_id)
        songs = [{"name": track['track']['name'], "artist": track['track']['artists'][0]['name']}
                 for track in playlist['tracks']['items']]
        return jsonify({'songs': songs})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download_song', methods=['POST'])
def download_song():
    """Download a specific song."""
    data = request.json
    song_name = data.get('song_name')
    artist_name = data.get('artist_name')
    try:
        downloaded_songs = getDownloadedSongs()
        song_key = f"{song_name} by {artist_name}"
        if song_key in downloaded_songs:
            return jsonify({'message': f"{song_name} by {artist_name} is already downloaded."})
        downloadSong(song_name, artist_name)
        getNewSong(song_name, artist_name)
        return jsonify({'message': f"Downloaded {song_name} by {artist_name}."})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
