from flask import Flask, request, render_template_string, session, redirect, url_for
import locale

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Kunci rahasia untuk session

# Set locale untuk pemformatan angka
locale.setlocale(locale.LC_ALL, '')

def format_rupiah(value):
    try:
        return "Rp. " + locale.format_string("%d", value, grouping=True)
    except ValueError:
        return "Rp. 0"

@app.route('/', methods=['GET', 'POST'])
def index():
    # Inisialisasi riwayat dan total jika belum ada di session
    if 'history' not in session:
        session['history'] = []
        session['total'] = 0  # Pastikan total diinisialisasi sebagai integer
        session['mode'] = 'add'  # Set mode default

    # Handle input baru
    if request.method == 'POST':
        nilai = request.form.get('nilai', '')
        mode = request.form.get('mode', session['mode'])  # Ambil mode dari form atau dari session

        try:
            nilai = int(nilai)
            if mode == 'add':
                total = session.get('total', 0) + nilai
            elif mode == 'subtract':
                total = session.get('total', 0) - nilai
            session['total'] = total  # Update total di session
            session['mode'] = mode  # Simpan mode ke session

            # Tambah riwayat baru ke session
            session['history'].append({
                'nilai': nilai,
                'total': total,
                'mode': 'Penambahan' if mode == 'add' else 'Pengurangan'
            })

            hasil = format_rupiah(total)  # Tampilkan hasil terbaru

        except ValueError:
            hasil = "Masukkan angka yang valid"

    elif request.args.get('action') == 'clear':
        session.pop('history', None)
        session.pop('total', None)
        session.pop('mode', None)
        return redirect(url_for('index'))

    else:
        hasil = None

    form_html = '''
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            background-color: #F3F7EC; /* Background utama */
        }
        .navbar {
            background-color: #006989; /* Navbar background color */
            overflow: hidden;
            position: sticky;
            top: 0;
            width: 100%;
            z-index: 1000;
        }
        .navbar a {
            float: left;
            display: block;
            color: #F3F7EC; /* Navbar link color */
            text-align: center;
            padding: 14px 20px;
            text-decoration: none;
            position: relative;
            z-index: 1;
        }
        .navbar a::before {
            content: "";
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            background: radial-gradient(circle, rgba(232,141,103,1) 0%, rgba(101,197,211,1) 100%); /* Gradiasi */
            border-radius: 50%;
            transform: translate(-50%, -50%);
            transition: width 0.4s ease, height 0.4s ease;
            z-index: -1;
        }
        .navbar a:hover::before {
            width: 150%;
            height: 150%;
        }
        .navbar a:hover {
            color: white;
        }
        form {
            background-color: white;
            padding: 20px;
            margin: 20px auto;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            max-width: 400px;
            display: flex;
            flex-direction: column;
            align-items: flex-start;
        }
        .button-container {
            margin-bottom: 10px;
        }
        .mode-button {
            display: inline-block;
            transition: all 0.2s ease-in;
            position: relative;
            overflow: hidden;
            z-index: 1;
            color: #090909;
            padding: 0.7em 1.7em;
            cursor: pointer;
            font-size: 18px;
            border-radius: 0.5em;
            background: #e8e8e8;
            border: 1px solid #e8e8e8;
            box-shadow: 6px 6px 12px #c5c5c5, -6px -6px 12px #ffffff;
        }
        .mode-button.active {
            background-color: #d2601a;
        }
        .mode-button:hover {
            background-color: #c57d4a; /* Button hover color */
        }
        .input-container {
            display: flex;
            align-items: center;
            width: 100%;
        }
        input[type="text"] {
            width: calc(100% - 50px);
            padding: 10px;
            margin: 10px 0;
            box-sizing: border-box;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        input[type="submit"], .clear-btn {
            background-color: #E88D67; /* Button background color */
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            margin-left: 10px;
            transition: background-color 0.3s ease;
        }
        input[type="submit"]:hover, .clear-btn:hover {
            background-color: #c57d4a; /* Button hover color */
        }
        .clear-btn {
            background-color: #E88D67;
            color: white;
            width: 30px;
            height: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            font-size: 16px;
            margin-left: 10px;
            text-decoration: none;
            transition: background-color 0.3s ease;
        }
        .clear-btn:hover {
            background-color: #ff4d4d; /* Clear button hover color */
        }
        .result, .history {
            margin-top: 20px;
            padding: 20px;
            background-color: #F3F7EC; /* Background color for results and history */
            border: 1px solid #ccc;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            max-width: 400px;
            margin: 20px auto;
        }
        .result {
            border-left: 6px solid #006989; /* Border color for result */
        }
        .history {
            border-left: 6px solid #E88D67; /* Border color for history */
        }
        .history ul {
            list-style-type: decimal;
            padding: 0;
        }
        .history li {
            padding: 5px 0;
        }
        .total {
            font-weight: bold;
            margin-top: 10px;
        }
    </style>

    <div class="navbar">
        <a href="/">Home</a>
        <a href="/about">About</a>
    </div>

    <form method="post">
        <div class="button-container">
            <button type="button" class="mode-button {{ 'active' if session['mode'] == 'add' else '' }}" onclick="setMode('add')">+</button>
            <button type="button" class="mode-button {{ 'active' if session['mode'] == 'subtract' else '' }}" onclick="setMode('subtract')">-</button>
        </div>

        <div class="input-container">
            <label for="nilai">Masukkan nilai:</label>
            <input type="text" id="nilai" name="nilai">
            <a href="/?action=clear" class="clear-btn" title="Clear Riwayat">🗑️</a>
        </div>
        <input type="hidden" name="mode" id="mode" value="{{ session['mode'] }}"> <!-- Default mode diambil dari session -->
        <input type="submit" value="Simpan">
    </form>
    '''

    if hasil is not None:
        form_html += f'<div class="result">Hasil: {hasil}</div>'

    # Tampilkan riwayat
    if session['history']:
        form_html += '<div class="history"><h3>Riwayat Nilai:</h3><ul>'
        for entry in session['history']:
            formatted_nilai = format_rupiah(entry['nilai'])
            formatted_total = format_rupiah(entry['total'])
            form_html += f'<li>{formatted_nilai} = {formatted_total}</li>'
        form_html += f'</ul><div class="total">Total Keseluruhan: {format_rupiah(session["total"])}</div></div>'

    form_html += '''
    <script>
        function setMode(mode) {
            document.getElementById('mode').value = mode;
            var buttons = document.getElementsByClassName('mode-button');
            for (var i = 0; i < buttons.length; i++) {
                buttons[i].classList.remove('active');
            }
            event.target.classList.add('active');
        }
    </script>
    '''

    return render_template_string(form_html)

@app.route('/about')
def about():
    about_html = '''
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            background-color: #F3F7EC; /* Background utama */
        }
        .navbar {
            background-color: #006989; /* Navbar background color */
            overflow: hidden;
            position: sticky;
            top: 0;
            width: 100%;
            z-index: 1000;
        }
        .navbar a {
            float: left;
            display: block;
            color: #F3F7EC; /* Navbar link color */
            text-align: center;
            padding: 14px 20px;
            text-decoration: none;
            position: relative;
            z-index: 1;
        }
        .navbar a::before {
            content: "";
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            background: radial-gradient(circle, rgba(232,141,103,1) 0%, rgba(101,197,211,1) 100%); /* Gradiasi */
            border-radius: 50%;
            transform: translate(-50%, -50%);
            transition: width 0.4s ease, height 0.4s ease;
            z-index: -1;
        }
        .navbar a:hover::before {
            width: 150%;
            height: 150%;
        }
        .navbar a:hover {
            color: white;
        }
        .content {
            padding: 20px;
            max-width: 800px;
            margin: auto;
            background-color: white;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
    </style>

    <div class="navbar">
        <a href="/">Home</a>
        <a href="/about">About</a>
    </div>

    <div class="content">
        <h1>Sejarah Kalkulator</h1>
        <p>Kalkulator adalah alat yang digunakan untuk melakukan perhitungan matematika. Sejarahnya dimulai sejak zaman kuno dengan alat-alat sederhana seperti abakus...</p>
        <p>Dengan kemajuan teknologi, kalkulator menjadi lebih kompleks dan dapat melakukan berbagai operasi aritmatika serta fungsi matematika canggih lainnya. Kalkulator digital pertama kali diperkenalkan pada tahun 1960-an dan terus berkembang hingga saat ini...</p>
        <p>Untuk informasi lebih lanjut, silakan kunjungi situs web kami atau hubungi kami melalui formulir kontak.</p>
    </div>
    '''

    return render_template_string(about_html)

if __name__ == '__main__':
    app.run(debug=True)
