# Tahap 1: Pilih base image
# Menggunakan image resmi Python versi 3.9 yang slim (ukuran kecil)
FROM python:3.9-slim

# Tahap 2: Atur lingkungan kerja di dalam container
WORKDIR /app

# Tahap 3: Install dependensi
# Salin file requirements.txt terlebih dahulu untuk memanfaatkan Docker cache.
# Jika file ini tidak berubah, Docker tidak akan menginstall ulang dependensi setiap kali build.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Tahap 4: Salin kode aplikasi Anda
# Menyalin semua file dan folder dari direktori proyek Anda ke dalam container di /app
COPY . .

# Tahap 5: Perintah untuk menjalankan aplikasi
# Gunicorn adalah server production untuk aplikasi Python, jauh lebih baik dari server bawaan Flask.
# --bind 0.0.0.0:8080: Membuat server bisa diakses dari luar container pada port 8080.
# src.server:app: Memberi tahu Gunicorn untuk menjalankan variabel 'app' dari file 'server.py' yang ada di dalam modul (folder) 'src'.
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--threads", "8", "--timeout", "120", "src.server:app"]