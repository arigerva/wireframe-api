from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/generate-wireframe', methods=['POST'])
def generate_wireframe():
    data = request.json
    return jsonify({"message": "Wireframe in creazione!", "figma_link": "https://www.figma.com/file/TUO_FILE_ID"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
