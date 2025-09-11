import os
import requests
import pandas as pd

API_URL = 'https://backend-python-sahabat-gula-166777420148.asia-southeast1.run.app/model/predict'
TEST_DIR = 'test/data'
TOP_N = 5

results = []

for label in os.listdir(TEST_DIR):
    label_dir = os.path.join(TEST_DIR, label)
    if not os.path.isdir(label_dir):
        continue

    correct_count = 0
    total_count = 0

    for img_name in os.listdir(label_dir):
        img_path = os.path.join(label_dir, img_name)
        if not img_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue

        if not os.path.exists(img_path):
            print(f"⚠️ File not found: {img_path}")
            continue

        try:
            with open(img_path, 'rb') as f:
                files = {'image': f}
                response = requests.post(API_URL, files=files)
        except Exception as e:
            print(f"[{img_name}] ❌ Request error: {e}")
            continue

        total_count += 1

        if response.status_code == 200:
            resp_json = response.json()
            best = resp_json.get('best', {})
            top_preds = resp_json.get('prediction', [])

            is_correct = best.get('slug', '') == label
            if is_correct:
                correct_count += 1

            results.append({
                'true_label': label,
                'filename': img_name,
                'prediction_label': best.get('slug', ''),
                'prediction_name': best.get('name', ''),
                'confidence': round(best.get('confidence', 0.0), 4),
                'is_correct': is_correct,
                'top_predictions': str(top_preds)
            })

            print(f"[{img_name}] True: {label} → Pred: {best.get('slug')} ({'🥰' if is_correct else '🐒'})")

        else:
            results.append({
                'true_label': label,
                'filename': img_name,
                'prediction_label': None,
                'prediction_name': None,
                'confidence': None,
                'is_correct': False,
                'top_predictions': f"ERROR {response.status_code}: {response.text}"
            })
            print(f"[{img_name}] Error: {response.text}")

    print(f"📊 Label {label}: {correct_count}/{total_count} correct ({(correct_count/total_count*100) if total_count else 0:.2f}%)\n")

# Simpan hasil
df = pd.DataFrame(results)
df.to_csv('test/evaluation_results.csv', index=False)
df.to_json('test/evaluation_results.json', orient='records', lines=False, indent=2)

print("\n✅ Evaluasi selesai!")
print(f"Total: {len(df)}")
print(f"Correct: {df['is_correct'].sum()}")
print(f"Accuracy: {df['is_correct'].mean()*100:.2f}%")
