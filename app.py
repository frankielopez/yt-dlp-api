from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return 'API is live! Use /download?url=VIDEO_URL'

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'Missing URL'}), 400

    ydl_opts = {
        'quiet': True,
        'format': 'best',
        'skip_download': True,
        'forceurl': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({
                'title': info.get('title'),
                'url': info.get('url'),
                'ext': info.get('ext'),
                'thumbnail': info.get('thumbnail'),
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

