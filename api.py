import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configura il token di accesso e l'ID del file Figma
FIGMA_ACCESS_TOKEN = os.getenv("FIGMA_ACCESS_TOKEN")  # ⬅️ Legge il token da Render
FIGMA_FILE_ID = os.getenv("FIGMA_FILE_ID")  # ⬅️ Legge l'ID del file da Render

# Funzione per creare un nodo in Figma
def create_figma_node(name, x, y, width, height, color):
    return {
        "name": name,
        "type": "FRAME",
        "absoluteBoundingBox": {
            "x": x,
            "y": y,
            "width": width,
            "height": height
        },
        "fills": [{
            "type": "SOLID",
            "color": color
        }]
    }

# Funzione per inviare i dati a Figma usando l'endpoint "post component sets"
def send_to_figma(elements):
    headers = {
        "X-Figma-Token": FIGMA_ACCESS_TOKEN,
        "Content-Type": "application/json"
    }
    
    figma_api_url = f"https://api.figma.com/v1/files/{FIGMA_FILE_ID}/components"
    
    payload = {
        "components": elements
    }

    response = requests.post(figma_api_url, headers=headers, json=payload)

    if response.status_code == 200:
        return f"https://www.figma.com/file/{FIGMA_FILE_ID}"
    else:
        print("Errore API Figma:", response.json())  # Debugging
        return None

@app.route('/generate-wireframe', methods=['POST'])
def generate_wireframe():
    data = request.json
    text = data.get("text", "")

    # Creiamo elementi in base alla richiesta del GPT
    elements = []

    if "navbar" in text.lower():
        elements.append(create_figma_node("Navbar", 100, 50, 800, 60, {"r": 0, "g": 0, "b": 0}))

    if "form" in text.lower():
        elements.append(create_figma_node("Form di Login", 150, 200, 400, 300, {"r": 0.9, "g": 0.9, "b": 0.9}))

    if not elements:
        return jsonify({"error": "Nessun elemento riconosciuto nella richiesta"}), 400

    figma_link = send_to_figma(elements)

    if figma_link:
        return jsonify({
            "message": "Wireframe generato con successo!",
            "figma_link": figma_link
        })
    else:
        return jsonify({"error": "Errore nella generazione del wireframe"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
