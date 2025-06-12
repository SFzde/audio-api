from flask import Flask, request, jsonify
from yt_dlp import YoutubeDL
import os

app = Flask(__name__)

@app.before_first_request
def create_cookie_file():
    # Solo crea cookies.txt si no existe y la variable está definida
    cookie_data = os.getenv("YOUTUBE_COOKIES")
    if cookie_data and not os.path.exists("cookies.txt"):
        with open("cookies.txt", "w", encoding='utf-8') as f:
            f.write(cookie_data)

@app.route('/get-audio-url')
def get_audio_url():
    video_url = request.args.get('q')
    if not video_url:
        return 'Falta el parámetro q', 400

    ydl_opts = {
        'quiet': True,
        'format': 'bestaudio[ext=webm]/bestaudio',
        'skip_download': True,
        'cookiefile': 'cookies.txt'
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            audio_url = info['url']
            return jsonify({'audioUrl': audio_url})
    except Exception as e:
        print(f"Error: {e}")
        return 'No se pudo obtener la URL de audio', 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
