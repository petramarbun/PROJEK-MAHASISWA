from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    form_html = '''
    <form action="/calculate" method="post">
        Angka pertama: <input type="text" name="angka1"><br>
        Angka kedua: <input type="text" name="angka2"><br>
        <input type="submit" value="Hitung">
    </form>
    '''
    return render_template_string(form_html)

@app.route('/calculate', methods=['POST'])
def calculate():
    angka1 = request.form['angka1']
    angka2 = request.form['angka2']

    # Mengubah input menjadi integer dan melakukan operasi aritmatika
    hasil = int(angka1) + int(angka2)

    return f"Hasil dari {angka1} + {angka2} adalah {hasil}"

if __name__ == '__main__':
    app.run(debug=True)
