from flask import Flask, render_template, request, jsonify
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests

cid = "4607d4d6a2eb461b82bc4acc0cbbe252"
secret = "213a8a1f76ca4929aebf235fa8cb8c89"

app = Flask(__name__)

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommendations', methods=['POST'])
def recommendations():
    seed_artist = request.form.get('artist')
    seed_track = request.form.get('track')
    
    if not seed_artist and not seed_track:
        return "Please provide an artist or track"

    seed_artists = []
    seed_tracks = []

    if seed_artist:
        artist_results = sp.search(q='artist:' + seed_artist, type='artist')
        if artist_results['artists']['items']:
            seed_artists.append(artist_results['artists']['items'][0]['id'])

    if seed_track:
        track_results = sp.search(q='track:' + seed_track, type='track')
        if track_results['tracks']['items']:
            seed_tracks.append(track_results['tracks']['items'][0]['id'])

    recommendations = sp.recommendations(seed_artists=seed_artists, seed_tracks=seed_tracks, limit=10)

    return render_template('recommendations.html', recommendations=recommendations['tracks'])

if __name__ == '__main__':
    app.run(debug=True, port=3000)
