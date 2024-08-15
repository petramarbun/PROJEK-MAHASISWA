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

    # Handle input baru
    if request.method == 'POST':
        nilai = request.form.get('nilai', '')
        mode = request.form.get('mode', 'add')  # Ambil mode dari form atau default ke 'add'

        try:
            nilai = int(nilai)
            if mode == 'add':
                total = session.get('total', 0) + nilai
            elif mode == 'subtract':
                total = session.get('total', 0) - nilai
            session['total'] = total  # Update total di session

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
        return redirect(url_for('index'))

    else:
        hasil = None

    form_html = '''
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            background-color: #fff1e1;
        }
        .navbar {
            background-color: #1d3c45;
            overflow: hidden;
            position: sticky;
            top: 0;
            width: 100%;
            z-index: 1000; /* Pastikan navbar tetap di atas elemen lain */
        }
        .navbar a {
            float: left;
            display: block;
            color: #f2f2f2;
            text-align: center;
            padding: 14px 20px;
            text-decoration: none;
        }
        .navbar a:hover {
            background-color: #ddd;
            color: black;
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
        .tabs {
            display: flex;
            cursor: pointer;
            border-bottom: 2px solid #1d3c45;
            margin-bottom: 10px;
            width: 100%;
        }
        .tab {
            flex: 1;
            padding: 10px;
            text-align: center;
            background-color: #f0f0f0;
            border: 1px solid #ddd;
            border-bottom: none;
            border-radius: 5px 5px 0 0;
            margin-right: 2px;
        }
        .tab.active {
            background-color: #ffffff;
            border-color: #1d3c45;
            font-weight: bold;
        }
        .tab-content {
            display: none;
            width: 100%;
        }
        .tab-content.active {
            display: block;
        }
        .input-container {
            display: flex;
            align-items: center;
            width: 100%;
        }
        input[type="text"] {
            width: calc(100% - 40px); /* Adjust width to accommodate smaller clear button */
            padding: 10px;
            margin: 10px 0;
            box-sizing: border-box;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        input[type="submit"], .clear-btn {
            background-color: #d2601a;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            margin-left: 10px;
        }
        input[type="submit"]:hover, .clear-btn:hover {
            background-color: #b24f14; /* Warna hover yang lebih gelap untuk tombol */
        }
        .clear-btn {
            background-color: #d2601a;
            color: white;
            width: 1px; /* Smaller width */
            height: 16px; /* Smaller height */
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            font-size: 14px; /* Smaller font size */
            margin-left: 10px;
            text-decoration: none;
        }
        .clear-btn:hover {
            background-color: #ff4d4d; /* Warna merah saat hover */
        }
        .result, .history {
            margin-top: 20px;
            padding: 20px;
            background-color: white;
            border: 1px solid #ccc;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            max-width: 400px;
            margin: 20px auto;
        }
        .result {
            border-left: 6px solid #1d3c45;
        }
        .history {
            border-left: 6px solid #d2601a;
        }
        .history ul {
            list-style-type: decimal; /* Ganti dengan decimal untuk nomor urut */
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
        <div class="tabs">
            <div class="tab active" onclick="openTab('add')">Tambah</div>
            <div class="tab" onclick="openTab('subtract')">Kurang</div>
        </div>

        <div id="add" class="tab-content active">
            <div class="input-container">
                <label for="nilai">Masukkan nilai:</label>
                <input type="text" id="nilai" name="nilai">
                <a href="/?action=clear" class="clear-btn" title="Clear Riwayat">🗑️</a>
            </div>
            <input type="hidden" name="mode" value="add">
        </div>

        <div id="subtract" class="tab-content">
            <div class="input-container">
                <label for="nilai">Masukkan nilai:</label>
                <input type="text" id="nilai" name="nilai">
                <a href="/?action=clear" class="clear-btn" title="Clear Riwayat">🗑️</a>
            </div>
            <input type="hidden" name="mode" value="subtract">
        </div>

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
        function openTab(tabName) {
            var i, tabcontent, tabs;
            tabcontent = document.getElementsByClassName("tab-content");
            for (i = 0; i < tabcontent.length; i++) {
                tabcontent[i].style.display = "none";
            }
            tabs = document.getElementsByClassName("tab");
            for (i = 0; i < tabs.length; i++) {
                tabs[i].className = tabs[i].className.replace(" active", "");
            }
            document.getElementById(tabName).style.display = "block";
            document.querySelector(".tab." + tabName).className += " active";
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
            background-color: #fff1e1;
        }
        .navbar {
            background-color: #1d3c45;
            overflow: hidden;
            position: sticky;
            top: 0;
            width: 100%;
            z-index: 1000; /* Pastikan navbar tetap di atas elemen lain */
        }
        .navbar a {
            float: left;
            display: block;
            color: #f2f2f2;
            text-align: center;
            padding: 14px 20px;
            text-decoration: none;
        }
        .navbar a:hover {
            background-color: #ddd;
            color: black;
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
