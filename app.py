from flask import Flask

app = Flask(__name__)

# Mémoire simple : 1 commande BIP
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

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
