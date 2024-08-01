Tentu, saya bantu perbaiki panduannya agar tidak perlu melakukan fork. Berikut adalah versi yang telah diperbaiki:

## Proyek GitHub untuk Pemula

Selamat datang di proyek kami! Proyek ini adalah tempat yang bagus bagi pemula untuk belajar menggunakan Git dan GitHub. Di bawah ini adalah panduan langkah demi langkah untuk membantu Anda berkontribusi pada proyek ini **tanpa perlu melakukan fork**.

## Persyaratan

- Git harus diinstal di komputer Anda. [Cara menginstal Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- Akun GitHub. [Buat akun GitHub](https://github.com/join)

## Langkah 1: Clone Repository

1. Buka terminal atau command prompt di komputer Anda.
2. Clone repository :

    ```bash
    git clone https://github.com/petramarbun/PROJEK-MAHASISWA
    ```

3. Masuk ke direktori repository:

    ```bash
    cd PROJEK-MAHASISWA
    git init
    ```

## Langkah 2: Membuat Branch Baru

1. Pastikan Anda berada di branch `master` dan sinkron dengan repository utama:

    ```bash
    git branch -M master
    git checkout master
    git pull
    ```

2. Buat dan pindah ke branch baru untuk pekerjaan Anda:

    ```bash
    git checkout -b nama-branch-anda
    ```

## Langkah 3: Membuat Perubahan

1. Lakukan perubahan yang diperlukan pada file proyek di editor teks atau IDE pilihan Anda.
2. Simpan perubahan Anda.

## Langkah 4: Commit Perubahan

1. Tambahkan perubahan yang telah Anda buat ke staging area:

    ```bash
    git add .
    ```

2. Buat commit dengan pesan deskriptif:

    ```bash
    git commit -m "Deskripsi singkat perubahan yang Anda buat"
    ```

## Langkah 5: Push Perubahan

1. Push perubahan ke branch baru Anda di repository utama:

    ```bash
    git push origin nama-branch-anda
    ```

## Langkah 6: Membuat Pull Request

1. Buka repository kita di GitHub.
2. Klik tombol **Compare & pull request**.
3. Berikan judul dan deskripsi untuk pull request Anda.
4. Klik tombol **Create pull request**.

Selamat berkontribusi!


WAJIB:
Tambahkan remote upstream untuk menjaga repository tetap sinkron.


1. Jalankan perintah berikut:


```bash

git remote add origin https://github.com/petramarbun/PROJEK-MAHASISWA

git remote add upstream https://github.com/petramarbun/PROJEK-MAHASISWA

```


2. Untuk memastikan remote upstream telah ditambahkan, jalankan perintah berikut:


```bash

git remote -v

```


Anda seharusnya melihat output seperti ini:


```plaintext

origin https://github.com/petramarbun/PROJEK-MAHASISWA

origin https://github.com/petramarbun/PROJEK-MAHASISWA

upstream https://github.com/petramarbun/PROJEK-MAHASISWA

upstream https://github.com/petramarbun/PROJEK-MAHASISWA

```