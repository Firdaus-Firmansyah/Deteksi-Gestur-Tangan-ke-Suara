# Deteksi Gestur Tangan ke Suara (Hand Gesture to Speech)

Proyek ini adalah implementasi deteksi gestur tangan secara real-time menggunakan Python, OpenCV, dan MediaPipe. Ketika gestur tertentu terdeteksi, program akan mengeluarkan output suara yang sesuai menggunakan Google Text-to-Speech (gTTS) dan Pygame.

Project ini dibuat untuk mengenali 5 gestur spesifik dan merangkainya menjadi sebuah kalimat perkenalan.



## Fitur

* **Deteksi Real-time**: Menggunakan webcam untuk mendeteksi gestur tangan secara langsung.
* **Tracking Tangan**: Didukung oleh [MediaPipe Hands](https://google.github.io/mediapipe/solutions/hands.html) untuk pelacakan 21 titik landmark tangan.
* **Output Suara**: Menggunakan `gTTS` untuk menghasilkan audio dari teks dan `Pygame` untuk memutarnya.
* **Logika Cooldown**: Mencegah output suara berulang (spam) dengan menerapkan jeda waktu.
* **Kustomisasi Mudah**: Logika gestur dan teks ucapan dapat dengan mudah diubah.

## Gestur yang Dikenali & Output Suara

Program ini dikonfigurasi untuk mengenali gestur berikut:

| Gestur | Teks yang Diucapkan |
| :--- | :--- |
| **Peace Sign** (V) ✌️ | "Hello" |
| **Shaka Sign** (Hang loose) 🤙 | "Perkenalkan" |
| **OK Sign** 👌 | "nama saya" |
| **Rock On Sign** 🤘 | "Firdaus Firmansyah" |
| **Stop Sign** (Telapak terbuka) ✋ | "Terima kasih atas perhatiannya" |

## Kebutuhan Sistem

* Python 3.7+
* Webcam yang terhubung
* Koneksi internet (untuk `gTTS` pertama kali mengambil audio)

## Langkah-Langkah Implementasi

Berikut adalah cara untuk menginstal dan menjalankan proyek ini di komputer Anda sendiri.

### 1. Klone Repositori

Pertama, klone (download) repositori ini ke komputer lokal Anda.

```bash
git clone [https://github.com/NAMA_ANDA/NAMA_REPOSITORI_ANDA.git](https://github.com/NAMA_ANDA/NAMA_REPOSITORI_ANDA.git)
cd NAMA_REPOSITORI_ANDA
```

### 2. Buat Lingkungan Virtual (Opsional tapi Direkomendasikan)

Sangat disarankan untuk membuat *virtual environment* agar dependensi proyek tidak tercampur dengan instalasi Python global Anda.

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instal Dependensi

Instal semua pustaka (library) Python yang dibutuhkan dengan satu perintah:

```bash
pip install opencv-python mediapipe gtts pygame
```

* `opencv-python`: Untuk mengakses webcam dan memproses gambar.
* `mediapipe`: Untuk model deteksi dan pelacakan tangan.
* `gtts`: Untuk mengubah teks menjadi file audio MP3.
* `pygame`: Untuk memutar file audio MP3.

### 4. Jalankan Program

Setelah semua dependensi terinstal, Anda bisa langsung menjalankan skrip Python.

```bash
python nama_file_anda.py
```
*(Ganti `nama_file_anda.py` dengan nama file skrip Anda, contoh: `main.py`)*

---

### **PENTING: Pengaturan Webcam**

Skrip ini menggunakan `cv2.VideoCapture(1)`.

* Angka `1` biasanya merujuk pada **webcam eksternal** (seperti USB webcam).
* Jika Anda hanya menggunakan **webcam bawaan laptop**, ganti angka tersebut menjadi `0`.

**Cari baris ini:**
```python
cap = cv2.VideoCapture(1)
```

**Ubah menjadi `0` jika perlu:**
```python
cap = cv2.VideoCapture(0)
```
---

### 5. Cara Menggunakan

1.  Jalankan skrip. Sebuah jendela OpenCV akan muncul menampilkan feed webcam Anda.
2.  Arahkan tangan Anda ke kamera.
3.  Bentuk salah satu dari 5 gestur yang telah ditentukan.
4.  Program akan menggambar landmark di tangan Anda dan menampilkan status gestur.
5.  Dengarkan output suara yang sesuai.
6.  Tekan tombol **'q'** pada keyboard Anda (sambil jendela OpenCV aktif) untuk keluar dari program.

## Kustomisasi

Anda dapat dengan mudah mengubah proyek ini.

### Mengubah Teks Suara

Untuk mengubah apa yang diucapkan, cari bagian ini di loop utama (`while cap.isOpened():`) dan ubah teks di dalam fungsi `speak()`:

```python
          if current_state == "Peace Sign":
                speak("Ubah ini menjadi teks lain")
            elif current_state == "Shaka Sign":
                speak("Teks custom Anda di sini")
            # ... dan seterusnya
```

### Menambah Gestur Baru

Untuk menambah gestur baru, Anda perlu memodifikasi fungsi `get_hand_gesture(hand_landmarks)`:

1.  Tambahkan logika baru untuk mendeteksi posisi jari (landmark) gestur Anda.
2.  Tambahkan `return "Nama Gestur Baru"` di dalam logika tersebut.
3.  Tambahkan kondisi `elif current_state == "Nama Gestur Baru":` di loop utama untuk memicu `speak()`.
