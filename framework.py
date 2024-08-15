from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "aku sayang moonton, moonton sayang kami"

@app.route('/profile/<nama>')
def namakamu(nama):
    return "halo kamu %s" %nama

if __name__ == '__main__':
    app.run(debug=True)