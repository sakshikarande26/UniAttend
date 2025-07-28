from flask import Flask, render_template, request, jsonify, redirect, url_for
import cv2
import face_recognition
import numpy as np
import pandas as pd
import os
import datetime
from PIL import Image
import base64
import io

app = Flask(__name__)

# --- Face Recognition Logic ---
def load_known_faces(known_faces_folder):
    known_face_encodings = []
    known_face_names = []
    for person_folder in os.listdir(known_faces_folder):
        person_folder_path = os.path.join(known_faces_folder, person_folder)
        if os.path.isdir(person_folder_path):
            for filename in os.listdir(person_folder_path):
                if filename.endswith((".jpg", ".png")):
                    image_path = os.path.join(person_folder_path, filename)
                    try:
                        image = face_recognition.load_image_file(image_path)
                        encodings = face_recognition.face_encodings(image)
                        if encodings:
                            known_face_encodings.append(encodings[0])
                            known_face_names.append(person_folder)
                    except Exception as e:
                        print(f"Error loading image {image_path}: {e}")
    return known_face_encodings, known_face_names

known_faces_folder = "facesData"
known_face_encodings, known_face_names = load_known_faces(known_faces_folder)

# --- Attendance Data ---
attendance_file = 'attendance.csv'
if not os.path.exists(attendance_file):
    pd.DataFrame(columns=["Name", "Time"]).to_csv(attendance_file, index=False)

def record_attendance(name):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    df = pd.read_csv(attendance_file)
    # Check if the person has already been marked present today
    if not ((df['Name'] == name) & (df['Time'].str.startswith(now.strftime("%Y-%m-%d")))).any():
        new_entry = pd.DataFrame([[name, timestamp]], columns=["Name", "Time"])
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(attendance_file, index=False)
        return True
    return False

def process_and_recognize(image):
    rgb_image = image.convert('RGB')
    img_np = np.array(rgb_image)
    
    face_locations = face_recognition.face_locations(img_np)
    face_encodings = face_recognition.face_encodings(img_np, face_locations)
    
    recognized_names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
            if record_attendance(name):
                recognized_names.append(name)
    return recognized_names

# --- Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))
    if file:
        image = Image.open(file.stream)
        names = process_and_recognize(image)
        if names:
            return redirect(url_for('attendance'))
        else:
            return render_template('index.html', message="No new faces recognized or attendance already marked.")

@app.route('/capture', methods=['POST'])
def capture():
    data = request.get_json()
    image_data = base64.b64decode(data['image'].split(',')[1])
    image = Image.open(io.BytesIO(image_data))
    names = process_and_recognize(image)
    if names:
        return jsonify({'success': True, 'names': names})
    else:
        return jsonify({'success': False, 'message': 'No new faces recognized or attendance already marked.'})

@app.route('/attendance')
def attendance():
    df = pd.read_csv(attendance_file)
    records = df.to_dict('records')
    return render_template('attendance.html', records=records)

if __name__ == '__main__':
    app.run(debug=True)
