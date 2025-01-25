import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Legge il token di accesso e l'ID del file Figma dalle variabili d'ambiente
FIGMA_ACCESS_TOKEN = os.getenv("FIGMA_ACCESS_TOKEN")
FIGMA_FILE_ID = os.getenv("FIGMA_FILE_ID")

# URL API di Figma
FIGMA_API_BASE_URL = "https://api.figma.com/v1"

# Headers per autenticazione API Figma
HEADERS = {
    "X-Figma-Token": FIGMA_ACCESS_TOKEN,
    "Content-Type": "application/json"
}

# Funzione per creare un nuovo file Figma
def create_new_figma_file():
    url = f"{FIGMA_API_BASE_URL}/projects"
    payload = {
        "name": "Wireframe Generato da API"
    }
    
    response = requests.post(url, headers=HEADERS, json=payload)

    if response.status_code == 200:
        file_id = response.json().get("id")
        return file_id
    else:
        print("Errore nella creazione del file:", response.json())
        return None

# Funzione per aggiungere nodi al file Figma
def add_elements_to_figma(file_id, elements):
    url = f"{FIGMA_API_BASE_URL}/files/{file_id}/components"
    
    payload = {
        "components": elements
    }

    response = requests.post(url, headers=HEADERS, json=payload)

    if response.status_code == 200:
        return f"https://www.figma.com/file/{file_id}"
    else:
        print("Errore API Figma:", response.json())  # Debugging
        return None

@app.route('/generate-wireframe', methods=['POST'])
def generate_wireframe():
    data = request.json
    text = data.get("text", "")

    # Creiamo un nuovo file se non esiste già
    file_id = FIGMA_FILE_ID if FIGMA_FILE_ID else create_new_figma_file()

    if not file_id:
        return jsonify({"error": "Errore nella creazione del file Figma"}), 500

    # Definiamo gli elementi da aggiungere
    elements = []

    if "navbar" in text.lower():
        elements.append({
            "name": "Navbar",
            "type": "FRAME",
            "x": 100,
            "y": 50,
            "width": 800,
            "height": 60,
            "backgroundColor": {"r": 0, "g": 0, "b": 0}
        })

    if "form" in text.lower():
        elements.append({
            "name": "Form di Login",
            "type": "FRAME",
            "x": 150,
            "y": 200,
            "width": 400,
            "height": 300,
            "backgroundColor": {"r": 0.9, "g": 0.9, "b": 0.9}
        })

    if not elements:
        return jsonify({"error": "Nessun elemento riconosciuto nella richiesta"}), 400

    # Aggiungere gli elementi al file Figma
    figma_link = add_elements_to_figma(file_id, elements)

    if figma_link:
        return jsonify({
            "message": "Wireframe generato con successo!",
            "figma_link": figma_link
        })
    else:
        return jsonify({"error": "Errore nella generazione del wireframe"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
