import os
from flask import Flask, request, redirect
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

scope = "user-read-private user-read-email"

sp_oauth = SpotifyOAuth(client_id=CLIENT_ID,
                        client_secret=CLIENT_SECRET,
                        redirect_uri=REDIRECT_URI,
                        scope=scope)


@app.route('/')
def home():
    return '<h2>💚 Bienvenido a Lia Spotify 💚<br><a href="/login">Iniciar sesión con Spotify</a></h2>'


@app.route('/login')
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return "No se recibió el código de autenticación.", 400

    token_info = sp_oauth.get_access_token(code, as_dict=True)

    if not token_info or 'access_token' not in token_info:
        return "No se pudo obtener el token de acceso.", 400

    access_token = token_info['access_token']

    return f"<h3>🎧 Autenticado correctamente con token: {access_token}</h3>"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
