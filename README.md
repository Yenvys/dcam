# ✌️ dcam - Discord Vanish & Meme Camera (ADIOS!)

<p align="center">
  <strong>Kamera virtual interaktif untuk Discord, Zoom, dan Google Meet dengan efek legendaris: Pose dua jari (Peace Sign ✌️) lalu menghilang memudar ke udara seperti meme "Peace Out / NileseyyNiles"!</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776ab?style=flat-square&logo=python&logoColor=white" alt="Python 3.10+" />
  <img src="https://img.shields.io/badge/OpenCV-4.8+-5c3ee8?style=flat-square&logo=opencv&logoColor=white" alt="OpenCV" />
  <img src="https://img.shields.io/badge/MediaPipe-Tasks-00758f?style=flat-square&logo=google&logoColor=white" alt="MediaPipe" />
  <img src="https://img.shields.io/badge/OBS-VirtualCam-302f2f?style=flat-square&logo=obsstudio&logoColor=white" alt="OBS VirtualCam" />
  <img src="https://img.shields.io/badge/Discord-Ready-5865F2?style=flat-square&logo=discord&logoColor=white" alt="Discord Ready" />
</p>

---

## 📋 Daftar Isi
- [Tentang dcam](#-tentang-dcam)
- [Cara Kerja](#-cara-kerja)
- [Fitur Utama](#-fitur-utama)
- [Prasyarat](#-prasyarat)
- [Instalasi](#-instalasi)
- [Cara Menjalankan](#-cara-menjalankan)
- [Shortcut Keyboard](#-shortcut-keyboard-saat-kamera-aktif)
- [Argumen Baris Perintah (CLI Options)](#-argumen-baris-perintah-cli-options)
- [Panduan Pengaturan di Discord](#-panduan-pengaturan-di-discord)
- [Troubleshooting](#-troubleshooting)
- [Lisensi](#-lisensi)

---

## 💡 Tentang dcam

**dcam** (*Discord Cam / Disappear Cam*) adalah aplikasi webcam berbasis kecerdasan buatan (*AI Computer Vision*) yang mendeteksi pose gestur tangan dua jari (Peace / Victory Sign ✌️). 

Ketika kamu mengacungkan pose dua jari ke arah kamera:
1. AI mendeteksi pose secara *real-time*.
2. Segmentasi tubuh memisahkan kamu dari latar belakang (*background*).
3. Karakter kamu perlahan-lahan memudar (*fade out*) hingga lenyap sepenuhnya, menyisakan ruangan kosong seperti meme terkenal **"Two Fingers Peace Out / Adios"**!
4. Begitu tangan kamu diturunkan, kamu akan perlahan memudar kembali (*fade in*) ke dalam frame.

Video hasil olahan langsung diteruskan ke **Virtual Camera** sehingga bisa dipilih langsung sebagai input kamera di aplikasi apa pun (Discord, Google Meet, Zoom, OBS, dll).

---

## 🔬 Cara Kerja

```
[ Webcam Input ]
       │
       ▼
[ MediaPipe Gesture Recognizer ] ──► Deteksi Gestur Peace Sign (✌️)
       │
       ├──► Jari Terangkat? ──► Turunkan Opacity Tubuh (Alpha 1.0 -> 0.0)
       │
       ▼
[ MediaPipe Selfie Segmenter ] ──► Masking Siluet Tubuh (Confidence Mask)
       │
       ▼
[ Alpha Blending + Gaussian Blur ] ──► Penggabungan Frame Tubuh & Frame Background Bersih
       │
       ▼
[ PyVirtualCam / OBS Virtual Cam ] ──► Discord / Zoom / Google Meet
```

---

## ✨ Fitur Utama

- 🤖 **MediaPipe Vision Tasks**: Menggunakan arsitektur AI terbaru Google MediaPipe untuk pendeteksian gestur dan segmentasi tubuh berkecepatan tinggi.
- 🌫️ **Efek Lenyap Mulus (*Smooth Fade Blending*)**: Menggunakan perpaduan *alpha blending* dan *Gaussian blur smoothing* pada tepian tubuh agar efek menghilang tampak sinematik dan tidak kaku.
- 📹 **Integrasi Virtual Camera (OBS VirtualCam)**: Output video langsung terbaca sebagai perangkat kamera fisik di sistem operasi Windows.
- 🔁 **Otomatis Unduh Model AI**: Jika file model MediaPipe belum ada di folder `models/`, skrip akan otomatis mengunduhnya secara langsung dari Google Cloud Storage.
- 🎮 **Kontrol Interaktif (*Hotkeys*)**: Ganti background, cerminkan kamera (*flip/mirror*), atau sembunyikan HUD hanya dengan menekan tombol keyboard.

---

## ⚙️ Prasyarat

1. **Python 3.10 atau lebih baru**:
   Pastikan Python sudah terinstal di komputer Anda dan ditambahkan ke variabel lingkungan `PATH`.
2. **OBS Studio (Sangat Disarankan untuk Virtual Camera)**:
   Aplikasi ini memanfaatkan driver **OBS Virtual Camera** melalui library `pyvirtualcam`.
   - Unduh dan pasang [OBS Studio](https://obsproject.com/).
   - Setelah menginstal OBS Studio, fitur Virtual Camera di Windows akan otomatis aktif dan siap digunakan oleh `dcam`.
   *(Catatan: Jika OBS belum terpasang, `dcam` tetap bisa berjalan menampilkan jendela preview).*

---

## 🚀 Instalasi

1. **Clone repositori ini**:
   ```bash
   git clone https://github.com/Yenvys/dcam.git
   cd dcam
   ```

2. **(Opsional) Buat dan aktifkan Virtual Environment**:
   ```bash
   python -m venv .venv
   # Di Windows PowerShell:
   .venv\Scripts\Activate.ps1
   ```

3. **Install seluruh dependensi**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🎬 Cara Menjalankan

Cukup jalankan perintah berikut di terminal:
```bash
python dcam.py
```

Saat pertama kali dijalankan:
1. Skrip akan memastikan model AI tersedia di folder `models/`.
2. **PENTING**: Saat kamera pertama kali menyala, **segera menyingkirlah sejenak dari hadapan kamera** selama 1-2 detik agar sistem dapat mengambil foto latar belakang kosong (*clean background*).
3. Jika latar belakang belum sempat diambil atau ada orang lain yang lewat, cukup minggir sebentar dan tekan tombol keyboard **`b`** untuk memperbarui background.
4. Hadap ke kamera, angkat tangan pose dua jari **✌️**, dan nikmati efek menghilang ke antah berantah!

---

## ⌨️ Shortcut Keyboard (Saat Kamera Aktif)

Tekan tombol-tombol berikut pada jendela *preview* kamera:

| Tombol | Fungsi | Keterangan |
| :---: | :--- | :--- |
| **`b`** | **Update Background** | Ambil ulang foto background kosong (minggir dulu dari frame) |
| **`m`** | **Toggle Mirror** | Balik tampilan secara horizontal (kiri-kanan) |
| **`h`** | **Toggle HUD** | Tampilkan atau sembunyikan teks status & persentase opacity |
| **`q`** | **Quit** | Keluar dari aplikasi dan tutup kamera |

---

## ⚙️ Argumen Baris Perintah (CLI Options)

Kamu bisa menyesuaikan resolusi, kecepatan efek memudar, atau memilih perangkat kamera yang berbeda:

```bash
python dcam.py [OPTIONS]
```

### Opsi yang Tersedia:
- `--camera`, `-c` *(int, default: `0`)*: Index perangkat webcam (gunakan `1` atau `2` jika memakai kamera eksternal).
- `--width` *(int, default: `1280`)*: Lebar resolusi video frame.
- `--height` *(int, default: `720`)*: Tinggi resolusi video frame.
- `--fps` *(int, default: `30`)*: Frame per second virtual camera.
- `--fade-out-speed` *(float, default: `0.15`)*: Kecepatan menghilang saat pose ✌️ aktif (semakin besar semakin instan).
- `--fade-in-speed` *(float, default: `0.15`)*: Kecepatan muncul kembali saat pose ✌️ diturunkan.
- `--no-flip` *(flag)*: Jangan balik/cerminkan frame secara horizontal.

**Contoh Penggunaan Kustom**:
```bash
# Menggunakan kamera kedua, resolusi Full HD 1080p dengan efek menghilang super cepat:
python dcam.py --camera 1 --width 1920 --height 1080 --fade-out-speed 0.25
```

---

## 🎧 Panduan Pengaturan di Discord

1. Jalankan `python dcam.py`.
2. Buka aplikasi **Discord**.
3. Buka menu **User Settings** (ikon gerigi di samping avatar) ➔ **Voice & Video** (Suara & Video).
4. Gulir ke bawah ke bagian **Video Settings** ➔ **Camera**.
5. Pilih kamera bernama **`OBS Virtual Camera`**.
6. Tekan tombol **Test Video**. Sekarang ketika kamu bergabung ke voice channel Discord dan menyalakan kamera, efek menghilang akan langsung tampil di layar teman-temanmu!

---

## ❓ Troubleshooting

- **Kamera tidak mau terbuka (*Error Cannot open camera*)**:
  - Pastikan webcam Anda tidak sedang dikunci oleh aplikasi lain (tutup Discord, browser, atau Zoom terlebih dahulu sebelum menyalakan skrip).
  - Coba ganti index kamera: `python dcam.py --camera 1`.
- **Virtual Camera tidak muncul**:
  - Pastikan Anda sudah menginstal **OBS Studio**. OBS menyediakan driver virtual cam di tingkat sistem operasi Windows yang digunakan oleh `pyvirtualcam`.
- **Efek menghilang meninggalkan bayangan aneh**:
  - Pastikan pencahayaan ruangan stabil.
  - Minggir sejenak dari frame kamera dan tekan tombol **`b`** untuk memperbarui foto latar belakang.

---

## 📄 Lisensi

Proyek ini dibuat untuk hiburan, eksperimen Computer Vision, dan meme komunitas. Bebas dikembangkan lebih lanjut.

Dibuat oleh **[Yenvys](https://github.com/Yenvys)**.
