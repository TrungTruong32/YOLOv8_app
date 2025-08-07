from flask import Flask, render_template, request
from ultralytics import YOLO
import torch
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
import json

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
RESULT_FOLDER = 'static/results'
RESULT_JSON_FOLDER = 'static/results_json'


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER
app.config['RESULT_JSON_FOLDER'] = RESULT_JSON_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)
os.makedirs(RESULT_JSON_FOLDER, exist_ok=True)

# Load YOLOv8 pretrained model
model = YOLO('yolov8n.pt')

@app.route('/', methods=['GET', 'POST'])
def index():
    result_img_path = None
    if request.method == 'POST':
        file = request.files['image']
        if not file or file.filename == '':
            return render_template('index.html', error="Vui lòng chọn ảnh!", uploaded_images=get_uploaded_images())

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        upload_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(upload_path)

        results = model.predict(upload_path, save=False)
        result_path = os.path.join(RESULT_FOLDER, f"result_{filename}")
        results[0].save(filename=result_path)
        save_detection_json(results, filename)

        return render_template('index.html', result_img=result_path.replace("\\", "/"))

    return render_template('index.html')

@app.route('/uploads')
def uploads_page():
    images = get_uploaded_images()
    return render_template('uploads.html', images=images)

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    result_path = os.path.join(RESULT_FOLDER, f"result_{filename}")
    json_path = os.path.join(RESULT_JSON_FOLDER, f"result_{filename}.json")

    if os.path.exists(upload_path):
        os.remove(upload_path)
    if os.path.exists(result_path):
        os.remove(result_path)
    if os.path.exists(json_path):
        os.remove(json_path)

    return redirect(url_for('uploads_page'))


@app.route('/detect/<filename>')
def detect_existing(filename):
    upload_path = os.path.join(UPLOAD_FOLDER, filename)
    result_path = os.path.join(RESULT_FOLDER, f"result_{filename}")
    json_path = os.path.join(RESULT_JSON_FOLDER, f"result_{filename}.json")

    if not os.path.exists(result_path):
        results = model.predict(upload_path, save=False)
        results[0].save(filename=result_path)
        save_detection_json(results, filename)

    return render_template('result.html',
                           original=f"/{UPLOAD_FOLDER}/{filename}",
                           result=f"/{RESULT_FOLDER}/result_{filename}",
                           json=f"/{RESULT_JSON_FOLDER}/result_{filename}.json")

def get_uploaded_images():
    files = [f for f in os.listdir(UPLOAD_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    return sorted(
        [{"filename": f, "url": url_for('static', filename=f'uploads/{f}')} for f in files],
        key=lambda x: x["filename"]
    )
def save_detection_json(results, filename):
    detections = []
    for result in results:
        for box in result.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            xyxy = box.xyxy[0].tolist()
            detections.append({
                "class": model.names[cls_id],
                "confidence": round(conf, 3),
                "bbox": {
                    "x1": round(xyxy[0], 2),
                    "y1": round(xyxy[1], 2),
                    "x2": round(xyxy[2], 2),
                    "y2": round(xyxy[3], 2)
                }
            })

    json_path = os.path.join(app.config['RESULT_JSON_FOLDER'], f"result_{filename}.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(detections, f, indent=4, ensure_ascii=False)

@app.route('/search', methods=['GET'])
def search_by_label():
    query = request.args.get('label', '').strip().lower()
    matched_images = []

    if query:
        for file in os.listdir(app.config['RESULT_JSON_FOLDER']):
            if file.endswith(".json"):
                json_path = os.path.join(app.config['RESULT_JSON_FOLDER'], file)
                with open(json_path, 'r', encoding='utf-8') as f:
                    detections = json.load(f)
                    labels_in_image = [d['class'].lower() for d in detections]
                    if query in labels_in_image:
                        # Lấy tên ảnh gốc từ tên file json
                        image_name = file.replace("result_", "").replace(".json", "")
                        matched_images.append({
                            "filename": image_name,
                            "url": url_for('static', filename=f'uploads/{image_name}')
                        })

    return render_template('search.html', label=query, images=matched_images)


if __name__ == '__main__':
    app.run(debug=True)
