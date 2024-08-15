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

        try:
            nilai = int(nilai)
            total = session.get('total', 0) + nilai  # Gunakan session.get() untuk menghindari KeyError
            session['total'] = total  # Update total di session

            # Tambah riwayat baru ke session
            session['history'].append({
                'nilai': nilai,
                'total': total
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
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Calculator</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    </head>
    <body>
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
                align-items: flex-start; /* Agar elemen berada di sebelah kiri */
            }
            label {
                margin-bottom: 5px; /* Jarak antara label dan input field */
                font-weight: bold;
            }
            .input-container {
                display: flex;
                align-items: center;
                width: 100%;
            }
            .input-container input[type="text"] {
                flex: 1; /* Input field mengambil ruang yang tersedia */
                padding: 10px;
                margin-right: 10px; /* Jarak antara input dan tombol Clear */
                box-sizing: border-box;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            .clear-btn {
                background-color: #d2601a;
                border-radius: 50%; /* Membuat tombol menjadi bulat */
                width: 40px; /* Ukuran tombol bulat */
                height: 40px; /* Ukuran tombol bulat */
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.2em; /* Ukuran ikon */
                color: #fff; /* Warna ikon */
                text-align: center;
                margin-top: 0; /* Menghilangkan margin top agar sejajar dengan input field */
                padding: 0; /* Hapus padding default */
                border: none; /* Menghapus border default */
                cursor: pointer;
            }
            .clear-btn:hover {
                background-color: #b24f14; /* Warna hover yang lebih gelap untuk tombol */
            }
            input[type="submit"] {
                background-color: #d2601a;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                margin-top: 10px; /* Jarak antara tombol Simpan dan elemen di atasnya */
                display: block;
                width: 100%;
            }
            input[type="submit"]:hover {
                background-color: #b24f14; /* Warna hover yang lebih gelap untuk tombol */
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
            <label for="nilai">Masukkan nilai:</label>
            <div class="input-container">
                <input type="text" id="nilai" name="nilai">
                <a href="/?action=clear" class="clear-btn"><i class="fas fa-trash-alt"></i></a>
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

    form_html += '</body></html>'

    return render_template_string(form_html)

@app.route('/about')
def about():
    about_html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>About</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    </head>
    <body>
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
    </body>
    </html>
    '''

    return render_template_string(about_html)

if __name__ == '__main__':
    app.run(debug=True)
