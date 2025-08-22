import os
from PIL import Image

TEST_DIR = "test/data"

print("🔍 Mengecek file gambar di:", TEST_DIR)

for root, _, files in os.walk(TEST_DIR):
    for f in files:
        path = os.path.join(root, f)
        size = os.path.getsize(path)

        # cek ukuran file
        if size == 0:
            print(f"❌ Kosong: {path}")
            continue

        # cek apakah bisa dibuka dengan Pillow
        try:
            with Image.open(path) as img:
                img.verify()  # hanya verifikasi, tidak load penuh
        except Exception as e:
            print(f"⚠️ Tidak valid image: {path} ({e})")
        else:
            print(f"✅ OK: {path} (size={size} bytes)")
