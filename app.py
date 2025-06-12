from flask import Flask, send_file, jsonify, abort
import os
from threading import Thread
import time

app = Flask(__name__)

SOUNDS_DIR = "templates/sound"

# Liste les sons disponibles (fichiers .mp3 dans SOUNDS_DIR)
@app.route("/list-sounds")
def list_sounds():
    try:
        files = [f for f in os.listdir(SOUNDS_DIR) if f.endswith(".mp3")]
        return jsonify(files)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Indique s'il y a un son à jouer (ici on simule qu'il y en a un ou pas)
# On peut améliorer selon ton logique (par exemple un fichier "play_sound.txt" avec le nom)
@app.route("/check-sound")
def check_sound():
    files = [f for f in os.listdir(SOUNDS_DIR) if f.endswith(".mp3")]
    if files:
        return jsonify({"sound": files[0]})  # On prend le premier son dispo
    else:
        return jsonify({"sound": None})

# Envoi le son demandé, puis le supprime *après* envoi
@app.route("/get-sound/<sound_name>")
def get_sound(sound_name):
    filepath = os.path.join(SOUNDS_DIR, sound_name)
    if not os.path.exists(filepath):
        return abort(404)

    def remove_file_later(path):
        # Attendre 1s pour être sûr que la réponse a commencé à être envoyée
        time.sleep(1)
        try:
            os.remove(path)
            print(f"[PASSERELLE] Fichier supprimé: {path}")
        except Exception as e:
            print(f"[PASSERELLE] Erreur suppression: {e}")

    # Lance la suppression en arrière-plan
    Thread(target=remove_file_later, args=(filepath,)).start()

    return send_file(filepath, mimetype="audio/mpeg", as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
