import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Token API e ID del file Figma
FIGMA_ACCESS_TOKEN = os.getenv("FIGMA_ACCESS_TOKEN")
FIGMA_FILE_ID = os.getenv("FIGMA_FILE_ID")

# Headers API Figma
HEADERS = {
    "X-Figma-Token": FIGMA_ACCESS_TOKEN,
    "Content-Type": "application/json"
}

# Funzione per aggiungere un frame al file Figma
def add_frame_to_figma():
    url = f"https://api.figma.com/v1/files/{FIGMA_FILE_ID}/frames"

    payload = {
        "name": "Wireframe Login",
        "children": [
            {
                "name": "Navbar",
                "type": "FRAME",
                "absoluteBoundingBox": {
                    "x": 100,
                    "y": 50,
                    "width": 800,
                    "height": 60
                },
                "fills": [{
                    "type": "SOLID",
                    "color": {"r": 0, "g": 0, "b": 0}
                }]
            },
            {
                "name": "Form di Login",
                "type": "FRAME",
                "absoluteBoundingBox": {
                    "x": 150,
                    "y": 200,
                    "width": 400,
                    "height": 300
                },
                "fills": [{
                    "type": "SOLID",
                    "color": {"r": 0.9, "g": 0.9, "b": 0.9}
                }]
            }
        ]
    }

    response = requests.post(url, headers=HEADERS, json=payload)

    if response.status_code == 200:
        return f"https://www.figma.com/file/{FIGMA_FILE_ID}"
    else:
        print("Errore API Figma:", response.status_code, response.text)
        return None

@app.route('/generate-wireframe', methods=['POST'])
def generate_wireframe():
    figma_link = add_frame_to_figma()

    if figma_link:
        return jsonify({
            "message": "Wireframe generato con successo!",
            "figma_link": figma_link
        })
    else:
        return jsonify({"error": "Errore nella generazione del wireframe"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
