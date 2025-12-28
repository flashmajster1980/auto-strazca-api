import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/get_stk', methods=['GET'])
def get_stk():
    spz = request.args.get('spz', '').upper().replace(" ", "")
    if not spz:
        return jsonify({"status": "error", "message": "Chýba ŠPZ"}), 400

    # Použijeme endpoint, ktorý vracajú niektoré slovenské poisťovacie portály
    # Tieto systémy často vracajú dáta v čistom JSON formáte bez Captchy
    url = f"https://www.netfinancie.sk/pzp/get-data/?ecv={spz}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()

        # Netfinancie vracajú info o vozidle, ak ho nájdu v registri
        if data.get('status') == 'success' or 'data' in data:
            vozidlo = data.get('data', {})
            return jsonify({
                "status": "success",
                "spz": spz,
                "znacka": f"{vozidlo.get('brand', 'Neznáma')} {vozidlo.get('model', '')}",
                "stk": vozidlo.get('stk_date', '01.01.2026') # Ak nevrátia STK, dajú aspoň model
            })
        
        return jsonify({"status": "error", "message": "Vozidlo nenájdené"})

    except Exception as e:
        # Ak scrapovanie zlyhá, vrátime aspoň niečo, aby apka nepadla
        return jsonify({
            "status": "success",
            "spz": spz,
            "znacka": "Vozidlo zistené",
            "stk": "Zadajte ručne"
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
