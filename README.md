# Sahabat Gula - Model Prediction Service

API service untuk prediksi makanan olahan lokal menggunakan machine learning pada aplikasi Sahabat Gula.

## Fitur

- **Prediksi Makanan Lokal**: Dapat mengidentifikasi 60 jenis makanan olahan lokal dari gambar
- **Akurasi Tinggi**: Model memiliki tingkat akurasi 94%
- **Top 3 Prediksi**: Memberikan 3 prediksi teratas dengan tingkat confidence masing-masing
- **RESTful API**: Endpoint sederhana untuk integrasi dengan aplikasi utama

## Teknologi

- **Flask**: Web framework Python
- **TensorFlow/Keras**: Machine learning model
- **NumPy**: Numerical processing
- **PIL**: Image processing

## API Endpoint

### POST /model/predict

Upload gambar makanan untuk mendapatkan prediksi.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: file dengan key `image`

**Response:**
```json
{
  "prediction": [
    {
      "id": 0,
      "slug": "nasi_gudeg",
      "name": "Nasi Gudeg",
      "confidence": 0.95
    },
    ...
  ],
  "best": {
    "id": 0,
    "slug": "nasi_gudeg", 
    "name": "Nasi Gudeg",
    "confidence": 0.95
  },
  "status": "success"
}
```

## Menjalankan Service

```bash
python app.py
```

Service akan berjalan di `http://0.0.0.0:5000`