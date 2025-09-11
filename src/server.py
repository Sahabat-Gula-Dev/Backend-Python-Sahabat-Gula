from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import io
import json
import logging

logging.basicConfig(level=logging.INFO)

MODEL_PATH = 'src/models/model.h5'
CLASS_INDICES_PATH = 'src/class_indices.json'
IMG_SIZE = 224
TOP_N = 3

model = load_model(MODEL_PATH)

with open(CLASS_INDICES_PATH, 'r') as f:
    class_indices = json.load(f)

class_names = [label for label, idx in sorted(class_indices.items(), key=lambda x: x[1])]

app = Flask(__name__)

def predict_image(file_storage):
    img = image.load_img(io.BytesIO(file_storage.read()), target_size=(IMG_SIZE, IMG_SIZE))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0
    return model.predict(img_array)

def get_top_predictions(predictions, top_n=TOP_N):
    top_n_indices = np.argsort(predictions[0])[::-1][:top_n]
    return [
        {
            'id': int(i),
            'slug': class_names[i],
            'name': class_names[i].replace('_', ' ').title(),
            'confidence': float(predictions[0][i])
        }
        for i in top_n_indices
    ]

@app.route('/model/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({
            'error': 'No file part with key "image"',
            'status': 'failed',
        }), 400
    
    file = request.files['image']

    if file.filename == '':
        return jsonify({
            'error': 'No selected file',
            'status': 'failed',
        }), 400

    try:
        preds = predict_image(file)
        top_preds = get_top_predictions(preds, TOP_N)

        return jsonify({
            'prediction': top_preds,
            'best': top_preds[0] if top_preds else None,
            'status': 'success'
        }), 200
    
    except Exception as e:
        app.logger.error(f"Error processing image: {e}", exc_info=True)
        return jsonify({
            'error': f'Failed to process image: {str(e)}',
            'status': 'failed',
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)