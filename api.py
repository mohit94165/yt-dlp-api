from flask import Flask, request, send_file
import yt_dlp, os

app = Flask(__name__)

@app.route("/download")
def download_video():
    url = request.args.get("url")
    if not url:
        return {"error": "No URL"}

    ydl_opts = {
        'format': 'bv*+ba/b',
        'merge_output_format': 'mp4',
        'outtmpl': 'video.%(ext)s',
        'quiet': True,
        'noplaylist': True,
        'http_headers': {'User-Agent': 'Mozilla/5.0'},
        'extractor_args': {'youtube': {'player_client': ['android']}}
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_name = ydl.prepare_filename(info)
        file_name = file_name.rsplit(".", 1)[0] + ".mp4"

    return send_file(file_name, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
