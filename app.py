from flask import Flask
app = Flask(__name__)

# simple mémoire (non persistante)
COMMAND = None

@app.route("/trigger")
def trigger():
    global COMMAND
    COMMAND = "BIP"
    return "Commande BIP enregistrée", 200

@app.route("/check")
def check():
    global COMMAND
    if COMMAND == "BIP":
        COMMAND = None
        return "BIP", 200
    return "NO", 204
