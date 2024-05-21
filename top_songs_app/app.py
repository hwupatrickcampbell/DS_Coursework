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
    
@app.route('/get_country', methods=['GET'])
def get_country():    
    api = 'https://ipinfo.io/json'
    response = requests.get(api)

    data = response.json()

    return data.get('country')

@app.route('/get_top_songs', methods=['POST'])
def get_top_songs():
    name = request.form.get('artist')
    market = request.form.get('market')
    
    if not market:
        market = get_country()

    results = sp.search(q='artist:' + name, type='artist')
    if not results['artists']['items']:
        return "Enter an artist"

    artist = results['artists']['items'][0]

    top_songs = sp.artist_top_tracks(artist['id'], country=market)['tracks']

    return render_template('top_songs.html', name=artist['name'], songs=top_songs)

if __name__ == '__main__':
    app.run(debug=True, port=80)
