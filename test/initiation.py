import os
import json

CLASS_INDICES_PATH = 'src/class_indices.json'
TEST_DIR = 'test/data'

with open(CLASS_INDICES_PATH, 'r') as f:
  class_indices = json.load(f)

os.makedirs(TEST_DIR, exist_ok=True)

for label in class_indices.keys():
  folder_path = os.path.join(TEST_DIR, label)
  os.makedirs(folder_path, exist_ok=True)
  print(f"Created folder: {folder_path}")

print("All folders created successfully.")