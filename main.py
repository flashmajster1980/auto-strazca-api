from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)
CORS(app)

def scraper_stk(spz):
    # Toto je príklad adresy, ktorú skúsime prečítať
    # POZNÁMKA: Scrapovanie štátnych webov vyžaduje neustálu údržbu kódu
    url = f"https://www.stkonline.sk/vyhladavanie-stk?spz={spz}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Tu hľadáme dátum v HTML kóde stránky
            # Tento selektor sa musí zhodovať s tým, čo má web v kóde
            text_stranky = soup.get_text()
            
            # Hľadáme dátum vo formáte DD.MM.YYYY
            najdeny_datum = re.search(r'\d{2}\.\d{2}\.\d{4}', text_stranky)
            
            if najdeny_datum:
                return najdeny_datum.group(0)
        return "Nenájdené (Web blokuje prístup)"
    except:
        return "Chyba spojenia"

@app.route('/get_stk', methods=['GET'])
def get_stk():
    spz = request.args.get('spz', '').upper().replace(" ", "")
    if not spz:
        return jsonify({"status": "error", "message": "Chýba ŠPZ"}), 400
    
    # Zavoláme náš scraper
    realny_datum = scraper_stk(spz)
    
    return jsonify({
        "status": "success",
        "spz": spz,
        "znacka": "Vozidlo " + spz,
        "stk": realny_datum
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
