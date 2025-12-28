from flask import Flask, jsonify, request
from flask_cors import CORS  # Dôležité, aby apka mohla komunikovať so serverom

app = Flask(__name__)
CORS(app)  # Toto povolí tvojej Flutter apke sťahovať dáta

@app.route('/')
def home():
    return "Server beží!"

@app.route('/get_stk', methods=['GET'])
def get_stk():
    spz = request.args.get('spz', '').upper()
    if not spz:
        return jsonify({"status": "error", "message": "Chýba ŠPZ"}), 400
    
    # TU príde neskôr ten zložitý kód na scraping. 
    # Teraz vrátime úspešnú odpoveď pre test apky.
    return jsonify({
        "status": "success",
        "spz": spz,
        "znacka": "Zistené vozidlo",
        "stk": "12.05.2026"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)