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
        @tailwind base;
        @tailwind components;
        @tailwind utilities;

        @layer base {
          :root {
            --background: 210 100% 97%;
            --foreground: 339 20% 20%;
            --primary: 308 56% 85%;
            --primary-foreground: 210 22% 22%;
            --secondary: 196 75% 88%;
            --secondary-foreground: 210 22% 22%;
            --accent: 211 86% 70%;
            --accent-foreground: 210 22% 22%;
            --destructive: 0 93% 73%;
            --destructive-foreground: 210 22% 22%;
            --muted: 210 100% 95%;
            --muted-foreground: 210 22% 22%;
            --card: 210 100% 97%;
            --card-foreground: 210 22% 22%;
            --popover: 0 0% 100%;
            --popover-foreground: 341 20% 22%;
            --border: 210 40% 80%;
            --input: 210 40% 56%;
            --ring: 210 40% 60%;
            --radius: 1rem;
          }
        }

        @layer base {
          * {
            @apply border-border;
          }

          body {
            @apply bg-background text-foreground font-body;
          }

          h1, h2, h3, h4, h5, h6 {
            @apply font-heading;
          }
        }

        .navbar {
            @apply bg-[#006989] overflow-hidden sticky top-0 w-full z-50;
        }

        .navbar a {
            @apply float-left block text-[#F3F7EC] text-center py-3 px-5 no-underline relative;
        }

        .navbar a::before {
            content: '';
            @apply absolute left-1/2 top-1/2 w-0 h-0 bg-gradient-to-r from-[#E88D67] to-transparent rounded-full transition-all duration-300 ease-in-out z-[-1];
        }

        .navbar a:hover::before {
            @apply w-full h-full left-0 top-0;
        }

        .navbar a:hover {
            @apply text-[#005C78];
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
            if (mode === 'add') {
                buttons[0].classList.add('active');
            } else if (mode === 'subtract') {
                buttons[1].classList.add('active');
            }
        }

        // Set default mode dari session
        setMode('{{ session["mode"] }}');
    </script>
    '''

    return render_template_string(form_html)

@app.route('/about')
def about():
    about_html = '''
    <style>
        @tailwind base;
        @tailwind components;
        @tailwind utilities;

        @layer base {
          :root {
            --background: 210 100% 97%;
            --foreground: 339 20% 20%;
            --primary: 308 56% 85%;
            --primary-foreground: 210 22% 22%;
            --secondary: 196 75% 88%;
            --secondary-foreground: 210 22% 22%;
            --accent: 211 86% 70%;
            --accent-foreground: 210 22% 22%;
            --destructive: 0 93% 73%;
            --destructive-foreground: 210 22% 22%;
            --muted: 210 100% 95%;
            --muted-foreground: 210 22% 22%;
            --card: 210 100% 97%;
            --card-foreground: 210 22% 22%;
            --popover: 0 0% 100%;
            --popover-foreground: 341 20% 22%;
            --border: 210 40% 80%;
            --input: 210 40% 56%;
            --ring: 210 40% 60%;
            --radius: 1rem;
          }
        }

        @layer base {
          * {
            @apply border-border;
          }

          body {
            @apply bg-background text-foreground font-body;
          }

          h1, h2, h3, h4, h5, h6 {
            @apply font-heading;
          }
        }

        .navbar {
            @apply bg-[#006989] overflow-hidden sticky top-0 w-full z-50;
        }

        .navbar a {
            @apply float-left block text-[#F3F7EC] text-center py-3 px-5 no-underline relative;
        }

        .navbar a::before {
            content: '';
            @apply absolute left-1/2 top-1/2 w-0 h-0 bg-gradient-to-r from-[#E88D67] to-transparent rounded-full transition-all duration-300 ease-in-out z-[-1];
        }

        .navbar a:hover::before {
            @apply w-full h-full left-0 top-0;
        }

        .navbar a:hover {
            @apply text-[#005C78];
        }
    </style>

    <div class="navbar">
        <a href="/">Home</a>
        <a href="/about">About</a>
    </div>

    <h1>About</h1>
    <p>This is the about page.</p>
    '''

    return render_template_string(about_html)

if __name__ == '__main__':
    app.run(debug=True)
