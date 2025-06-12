from flask import Flask, request, send_file
from io import BytesIO

app = Flask(__name__)

SOUND_DATA = None

@app.route("/upload", methods=["POST"])
def upload():
    global SOUND_DATA
    file = request.files.get("file")
    if file:
        SOUND_DATA = file.read()
        return "Fichier reçu", 200
    return "Aucun fichier", 400

@app.route("/check")
def check():
    if SOUND_DATA:
        return "READY", 200
    return "NO", 204

@app.route("/get-sound")
def get_sound():
    if not SOUND_DATA:
        return "Pas de son", 404
    return send_file(BytesIO(SOUND_DATA), mimetype="audio/mpeg", download_name="sound.mp3")
    
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
