from flask import Flask, request, jsonify, send_file
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploaded_sounds"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

current_sound = None  # nom du fichier son à jouer

@app.route("/upload-sound", methods=["POST"])
def upload_sound():
    global current_sound
    if 'file' not in request.files or 'sound' not in request.form:
        return "Fichier ou nom du son manquant", 400

    file = request.files['file']
    sound_name = request.form['sound']

    filepath = os.path.join(UPLOAD_FOLDER, sound_name)
    file.save(filepath)
    current_sound = sound_name
    return "Son reçu avec succès", 200

@app.route("/check-sound")
def check_sound():
    if current_sound:
        return jsonify({"sound": current_sound})
    else:
        return jsonify({"sound": None})

@app.route("/get-sound/<sound_name>")
def get_sound(sound_name):
    filepath = os.path.join(UPLOAD_FOLDER, sound_name)
    if os.path.exists(filepath):
        return send_file(filepath, mimetype="audio/mpeg")
    else:
        return "Son non trouvé", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
