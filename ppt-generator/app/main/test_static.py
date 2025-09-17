from flask import Flask
import os

app = Flask(
    __name__,
    static_folder="app/static",       # pastikan ini sesuai
    static_url_path="/static"
)

@app.route("/")
def home():
    return '<img src="/static/templates/classic.png">'

if __name__ == "__main__":
    print("Static folder:", os.path.abspath("app/static"))
    app.run(debug=True, port=5000)
