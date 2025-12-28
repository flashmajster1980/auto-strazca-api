from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Server beží a hľadá autá!"

@app.route('/get_stk', methods=['GET'])
def get_stk():
    spz = request.args.get('spz', '').upper().replace(" ", "")
    if not spz:
        return jsonify({"status": "error", "message": "Chýba ŠPZ"}), 400
    
    # REÁLNA LOGIKA (Ukážka pre princíp):
    # Skúsime nájsť info na webe, ktorý nemá extrémnu ochranu (napr. niektoré PZP vyhľadávače)
    # POZNÁMKA: Ak štátny web zmení kód, toto treba upraviť.
    
    try:
        # Pre testovacie účely vrátime inteligentný odhad, 
        # kým si nadefinuješ presnú URL adresu tvojho obľúbeného zdroja.
        # Ak by sme chceli reálne stiahnuť HTML:
        # r = requests.get(f"https://nejaky-web.sk/kontrola?spz={spz}")
        # soup = BeautifulSoup(r.text, 'html.parser')
        
        return jsonify({
            "status": "success",
            "spz": spz,
            "znacka": "Overené vozidlo", 
            "stk": "12.10.2026" # Tu by bol reálny dátum vytiahnutý z HTML
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
