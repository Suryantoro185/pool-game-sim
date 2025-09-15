# Game Biliar Sederhana dengan CoppeliaSim dan Python
Project ini adalah implementasi permainan biliar sederhana yang disimulasikan di **CoppeliaSim EDU** dan dikontrol secara *real-time* menggunakan skrip **Python**.
Pemain dapat mengatur arah dan kekuatan pukulan bola sodok melalui keyboard.
---

## Kebutuhan Sistem
Pastikan Anda memiliki perangkat lunak berikut sebelum memulai:
1.  **CoppeliaSim EDU**: Versi 4.3 atau yang lebih baru.
2.  **Python**: Versi 3.6 atau yang lebih baru.
3.  **Library ZMQ Client**: Library ini digunakan oleh Python untuk berkomunikasi dengan CoppeliaSim. Instal dengan perintah:
    ```bash
    pip install coppeliasim-zmqremoteapi-client
    ```
---

## 1. Pengaturan Scene di CoppeliaSim
Sebelum menjalankan skrip Python, siapkan *scene* Anda di CoppeliaSim dengan langkah-langkah berikut:

#### a. Buat Meja dan Bola
- Buat atau impor model meja biliar.
- Buat bola-bola biliar menggunakan bentuk `Sphere`. Pastikan bola sodok (*cue ball*) memiliki nama yang unik. Skrip ini secara default menggunakan nama `Sphere[6]` untuk bola sodok.

#### b. Atur Properti Fisika
- **Untuk Semua Bola**:
  - Pilih semua bola, buka dialog **Shape Dynamics Properties**.
  - Centang `Body is dynamic` dan `Respondable`.
- **Untuk Dinding Meja**:
  - Centang `Respondable` tetapi **JANGAN** centang `Body is dynamic`.

#### c. Buat Garis Bidik
- Tambahkan objek baru: **Add -> Primitive shape -> Cylinder**.
- Ubah ukurannya menjadi tipis dan panjang agar terlihat seperti garis.
- **Ganti nama objek ini menjadi `AimingLine`**. Skrip akan mencari objek dengan nama ini.
- Buka **Shape Dynamics Properties** untuk `AimingLine` dan **pastikan semua checkbox tidak dicentang**
---

## 2. Menjalankan Game
Setelah *scene* siap, ikuti langkah berikut untuk memulai permainan:
1.  **Simpan Kode**: Simpan skrip Python yang disediakan sebagai `billiard_game.py`.
2.  **Buka Scene**: Buka file *scene* biliar Anda di CoppeliaSim.
3.  **Jalankan Simulasi**: **Klik tombol Play di CoppeliaSim** untuk memulai simulasi. Skrip Python tidak dapat terhubung jika simulasi tidak berjalan.
4.  **Jalankan Skrip**: Buka terminal (CMD, PowerShell, atau Terminal), navigasi ke folder tempat Anda menyimpan file, dan jalankan perintah:
    ```bash
    python billiard_game.py
    ```
5.  **Mainkan**: Pindahkan fokus Anda ke jendela terminal untuk memasukkan perintah keyboard. Status game akan ditampilkan di *status bar* CoppeliaSim.
---

## Kontrol Permainan
Gunakan tombol berikut di jendela terminal untuk bermain:
-   `A` / `D` : Memutar arah bidikan ke kiri/kanan.
-   `W` / `S` : Menambah / mengurangi kekuatan pukulan.
-   `Spasi` : Menembak bola.
-   `Ctrl + C` : Menghentikan skrip/game.
