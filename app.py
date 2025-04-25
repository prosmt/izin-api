from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client
import os

# Supabase bilgileri
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)
CORS(app)  # CORS izinleri verildi

@app.route('/')
def home():
    return "İzin Sorgulama API Çalışıyor ✅"

@app.route('/sorgula', methods=['POST'])
def sorgula():
    data = request.get_json()
    ad_soyad = data.get('ad_soyad')
    tc_son3 = data.get('tc_son3')

    if not ad_soyad or not tc_son3:
        return jsonify({"error": "Ad Soyad ve TC Son 3 hane zorunlu."}), 400

    try:
        response = supabase.table('izinler')\
            .select("*")\
            .eq('ad_soyad', ad_soyad)\
            .eq('tc_son3', tc_son3)\
            .limit(1)\
            .execute()

        rows = response.data
        if rows and len(rows) > 0:
            kalan_izin = rows[0].get('kalan_izin_gunu', 0)
            return jsonify({"kalan_izin_gunu": kalan_izin})
        else:
            return jsonify({"error": "Kayıt bulunamadı."}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
