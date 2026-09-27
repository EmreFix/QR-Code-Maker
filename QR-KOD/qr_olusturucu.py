import qrcode
from PIL import Image
import io
import base64
import webbrowser
from flask import Flask, request, render_template_string
import threading
import logging
import os
import signal

app = Flask(__name__)

# Sunucu yazılarını gizleyerek açılışı hızlandırır
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Kullanıcı arayüzünü oluşturacak HTML ve CSS kodu
HTML_SABLON = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>QR Kod Oluşturucu</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #2c2f33; color: white; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
        .container { background: #23272a; padding: 40px; border-radius: 12px; box-shadow: 0 8px 16px rgba(0,0,0,0.5); text-align: center; max-width: 450px; width: 100%; border: 1px solid #444; position: relative; }
        h2 { margin-top: 0; color: #7289da; }
        input[type="text"] { width: 100%; padding: 12px; margin: 15px 0; border: none; border-radius: 6px; background-color: #40444b; color: white; box-sizing: border-box; font-size: 14px; }
        input[type="file"] { width: 100%; padding: 10px; margin: 5px 0 20px 0; background-color: #40444b; border-radius: 6px; color: #ccc; }
        button { background-color: #43b581; color: white; padding: 12px 20px; border: none; border-radius: 6px; cursor: pointer; font-size: 16px; font-weight: bold; width: 100%; transition: background-color 0.2s; margin-bottom: 10px; }
        button:hover { background-color: #3ca374; }
        .close-btn { background-color: #f04747; margin-top: 10px; }
        .close-btn:hover { background-color: #d84040; }
        .qr-result { margin-top: 30px; padding-top: 20px; border-top: 1px solid #444; }
        img { max-width: 100%; height: auto; border-radius: 8px; padding: 10px; background: white; }
        .info { font-size: 13px; color: #99aab5; margin-top: 10px; }
        label { display: block; text-align: left; font-size: 14px; color: #b9bbbe; margin-bottom: 5px; }
    </style>
    <script>
        function sunucuyuKapat() {
            fetch('/kapat').then(() => {
                document.body.innerHTML = '<h2 style="color:white; text-align:center; margin-top:20%;">Uygulama Kapatıldı.<br>Bu sekmeyi kapatabilirsiniz.</h2>';
                setTimeout(() => window.close(), 2000);
            });
        }
    </script>
</head>
<body>
    <div class="container">
        <h2>🔗 Linkten QR Koda</h2>
        <form method="POST" enctype="multipart/form-data">
            <input type="text" name="link" placeholder="Dönüştürülecek linki buraya yapıştır..." required>
            
            <label>Ortaya Logo Ekle (İsteğe Bağlı):</label>
            <input type="file" name="logo" accept="image/png, image/jpeg, image/jpg">
            
            <button type="submit">QR Kod Üret</button>
        </form>
        
        <!-- Sunucuyu arka planda kapatan buton -->
        <button class="close-btn" onclick="sunucuyuKapat()">❌ Uygulamayı Komple Kapat</button>

        {% if qr_image %}
            <div class="qr-result">
                <img src="data:image/png;base64,{{ qr_image }}" alt="Oluşturulan QR Kod">
                <p class="info">İndirmek için görsele sağ tıklayıp <b>"Resmi Farklı Kaydet"</b> seçeneğine tıkla.</p>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def ana_sayfa():
    qr_image = None
    if request.method == 'POST':
        link = request.form.get('link')
        logo_file = request.files.get('logo')

        qr = qrcode.QRCode(version=5, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
        qr.add_data(link)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

        if logo_file and logo_file.filename != '':
            try:
                logo = Image.open(logo_file)
                taban_genislik = int(img.size[0] / 3)
                oran = (taban_genislik / float(logo.size[0]))
                yukseklik = int((float(logo.size[1]) * float(oran)))
                if hasattr(Image, 'Resampling'):
                    logo = logo.resize((taban_genislik, yukseklik), Image.Resampling.LANCZOS)
                else:
                    logo = logo.resize((taban_genislik, yukseklik), Image.LANCZOS)
                pozisyon = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
                img.paste(logo, pozisyon)
            except Exception as e:
                print(f"Logo hatası: {e}")

        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        qr_image = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return render_template_string(HTML_SABLON, qr_image=qr_image)

@app.route('/kapat')
def kapat():
    # Butona basıldığında sunucuyu tamamen sonlandırır
    os.kill(os.getpid(), signal.SIGTERM)
    return "Kapandı"

def tarayiciyi_ac():
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    threading.Timer(0.1, tarayiciyi_ac).start()
    app.run(port=5000)