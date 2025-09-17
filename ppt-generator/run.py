import os
from flask import Flask
from flask_cors import CORS   # <--- tambahkan ini
from app.main.routes import main

# --- Inisialisasi Flask App ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, "app", "static"),      # lokasi static
    template_folder=os.path.join(BASE_DIR, "app", "templates"), # lokasi templates
    static_url_path="/static"
)

# --- Aktifkan CORS untuk semua route /api/*
CORS(app, resources={r"/api/*": {"origins": "*"}})

# --- Register Blueprint ---
app.register_blueprint(main)

# --- Konfigurasi optional ---
app.config['JSON_SORT_KEYS'] = False  # biar JSON response tidak di-sort
app.config['TEMPLATES_AUTO_RELOAD'] = True  # reload template saat development

# --- Main entrypoint ---
if __name__ == "__main__":
    # Jalankan server di localhost:5000
    app.run(host="0.0.0.0", port=5000, debug=True)
