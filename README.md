# Proyek GitHub untuk Pemula

Selamat datang di proyek kami! Proyek ini adalah tempat yang bagus bagi pemula untuk belajar menggunakan Git dan GitHub. Di bawah ini adalah panduan langkah demi langkah untuk membantu Anda berkontribusi pada proyek ini.

## Persyaratan

- Git harus diinstal di komputer Anda. [Cara menginstal Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- Akun GitHub. [Buat akun GitHub](https://github.com/join)

## Langkah 1: Fork Repository

1. Masuk ke akun GitHub Anda.
2. Buka halaman repository proyek ini.
3. Klik tombol **Fork** di sudut kanan atas layar. Ini akan membuat salinan repository ini di akun GitHub Anda.

## Langkah 2: Clone Repository

1. Buka terminal atau command prompt di komputer Anda.
2. Clone repository hasil fork ke komputer Anda dengan menjalankan perintah berikut (gantilah `your-username` dengan nama pengguna GitHub Anda):

    ```bash
    git clone https://github.com/your-username/nama-repo.git
    ```

3. Masuk ke direktori repository:

    ```bash
    cd nama-repo
    ```

## Langkah 3: Menambahkan Remote Upstream

Tambahkan remote upstream untuk menjaga repository fork Anda tetap sinkron dengan repository asli.

1. Jalankan perintah berikut:

    ```bash
    git remote add upstream https://github.com/original-username/nama-repo.git
    ```

2. Untuk memastikan remote upstream telah ditambahkan, jalankan perintah berikut:

    ```bash
    git remote -v
    ```

    Anda seharusnya melihat output seperti ini:

    ```plaintext
    origin  https://github.com/your-username/nama-repo.git (fetch)
    origin  https://github.com/your-username/nama-repo.git (push)
    upstream  https://github.com/original-username/nama-repo.git (fetch)
    upstream  https://github.com/original-username/nama-repo.git (push)
    ```

## Langkah 4: Membuat Branch Baru

1. Sebelum membuat branch baru, pastikan Anda berada di branch `main` dan sinkron dengan repository upstream:

    ```bash
    git checkout main
    git fetch upstream
    git merge upstream/main
    ```

2. Buat dan pindah ke branch baru untuk pekerjaan Anda:

    ```bash
    git checkout -b nama-branch-anda
    ```

## Langkah 5: Membuat Perubahan

1. Lakukan perubahan yang diperlukan pada file proyek di editor teks atau IDE pilihan Anda.
2. Simpan perubahan Anda.

## Langkah 6: Commit Perubahan

1. Tambahkan perubahan yang telah Anda buat ke staging area:

    ```bash
    git add .
    ```

2. Buat commit dengan pesan deskriptif:

    ```bash
    git commit -m "Deskripsi singkat perubahan yang Anda buat"
    ```

## Langkah 7: Push Perubahan

1. Push perubahan ke repository fork Anda di GitHub:

    ```bash
    git push origin nama-branch-anda
    ```

## Langkah 8: Membuat Pull Request

1. Buka repository fork Anda di GitHub.
2. Klik tombol **Compare & pull request**.
3. Berikan judul dan deskripsi untuk pull request Anda.
4. Klik tombol **Create pull request**.

## Langkah 9: Menjaga Fork Anda Tetap Sinkron

1. Setiap kali Anda ingin memperbarui fork Anda dengan perubahan terbaru dari repository asli, pastikan Anda berada di branch `main`:

    ```bash
    git checkout main
    ```

2. Ambil perubahan dari upstream dan gabungkan:

    ```bash
    git fetch upstream
    git merge upstream/main
    ```

3. Push perubahan ke repository fork Anda:

    ```bash
    git push origin main
    ```

## Bantuan

Jika Anda mengalami masalah atau memiliki pertanyaan, jangan ragu untuk membuka issue di repository ini atau menghubungi kami.

Selamat berkontribusi!
