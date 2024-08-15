from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    hasil = None
    if request.method == 'POST':
        angka1 = int(request.form['angka1'])
        angka2 = int(request.form['angka2'])
        operation = request.form['operation']

        if operation == 'Tambah':
            hasil = angka1 + angka2
        elif operation == 'Kurang':
            hasil = angka1 - angka2
        elif operation == 'Kali':
            hasil = angka1 * angka2
        elif operation == 'Bagi':
            if angka2 != 0:
                hasil = angka1 / angka2
            else:
                hasil = "Tidak bisa membagi dengan nol!"

    form_html = '''
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 50px;
            background-color: #f4f4f4;
        }
        form {
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        input[type="text"], select {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            box-sizing: border-box;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        input[type="submit"] {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        input[type="submit"]:hover {
            background-color: #45a049;
        }
        .result {
            margin-top: 20px;
            padding: 10px;
            background-color: #e7f3fe;
            border-left: 6px solid #2196F3;
        }
    </style>

    <form method="post">
        <label for="angka1">Angka pertama:</label>
        <input type="text" id="angka1" name="angka1"><br>
        
        <label for="angka2">Angka kedua:</label>
        <input type="text" id="angka2" name="angka2"><br>
        
        <label for="operation">Pilih Operasi:</label>
        <select id="operation" name="operation">
            <option value="Tambah">+</option>
            <option value="Kurang">-</option>
            <option value="Kali">*</option>
            <option value="Bagi">/</option>
        </select><br><br>
        
        <input type="submit" value="Hitung">
    </form>
    '''

    if hasil is not None:
        form_html += f'<div class="result">Hasil: {hasil}</div>'
    
    return render_template_string(form_html)

if __name__ == '__main__':
    app.run(debug=True)
