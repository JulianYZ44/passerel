from flask import Flask, request
import requests

app = Flask(__name__)

# URL du PC local où tourne test.py (il faut que ce soit accessible depuis le serveur)
LOCAL_PC_URL = "http://172.20.10.2:5001/beep"

@app.route('/app', methods=['POST'])
def passerelle():
    try:
        # On transmet la requête à test.py sur ton PC
        r = requests.post(LOCAL_PC_URL)
        if r.status_code == 200:
            return "Requête transmise au PC local"
        else:
            return "Erreur de transmission", 500
    except Exception as e:
        return f"Erreur: {str(e)}", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
