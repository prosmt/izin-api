from flask import Flask, request, jsonify
from supabase import create_client, Client
import os

app = Flask(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/sorgula', methods=['POST'])
def sorgula():
    data = request.get_json()
    ad_soyad = data.get('ad_soyad')
    tc_son3 = data.get('tc_son3')

    if not ad_soyad or not tc_son3:
        return jsonify({'error': 'Ad Soyad ve TC son 3 hanesi zorunludur.'}), 400

    response = supabase.table('izinler')\
        .select("*")\
        .eq('ad_soyad', ad_soyad)\
        .eq('tc_son3', tc_son3)\
        .single()\
        .execute()

    if response.data:
        kalan_izin = response.data['kalan_izin_gunu']
        return jsonify({'kalan_izin_gunu': kalan_izin}), 200
    else:
        return jsonify({'error': 'Kayıt bulunamadı.'}), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))