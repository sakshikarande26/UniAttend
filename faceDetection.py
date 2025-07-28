import streamlit as st
import cv2
import face_recognition
import numpy as np
import pandas as pd
import os
import datetime
from PIL import Image


# Load known face encodings and their names
def load_known_faces(known_faces_folder):
    known_face_encodings = []
    known_face_names = []

    for person_folder in os.listdir(known_faces_folder):
        person_folder_path = os.path.join(known_faces_folder, person_folder)

        if os.path.isdir(person_folder_path):
            for filename in os.listdir(person_folder_path):
                if filename.endswith(".jpg") or filename.endswith(".png"):
                    image_path = os.path.join(person_folder_path, filename)
                    image = face_recognition.load_image_file(image_path)
                    encoding = face_recognition.face_encodings(image)[0]
                    known_face_encodings.append(encoding)
                    known_face_names.append(person_folder)

    return known_face_encodings, known_face_names


# Function to process images and mark attendance
def process_image(image, attendance_df, known_face_encodings, known_face_names):
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_image)
    face_encodings = face_recognition.face_encodings(rgb_image, face_locations)

    if len(face_encodings) == 0:
        st.warning("No faces detected.")
        return

    for face_encoding, face_location in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

            now = datetime.datetime.now()
            # Record attendance
            attendance_df.loc[len(attendance_df)] = [name, now.strftime("%Y-%m-%d %H:%M:%S")]
            st.success(f"Attendance marked for {name} at {now.strftime('%Y-%m-%d %H:%M:%S')}.")

        top, right, bottom, left = face_location
        cv2.rectangle(rgb_image, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(rgb_image, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    st.image(rgb_image, caption="Captured Image", channels="RGB")


# Add a function to evaluate accuracy
def evaluate_accuracy(predictions, ground_truth):
    correct_predictions = sum([1 for pred, true in zip(predictions, ground_truth) if pred == true])
    accuracy = correct_predictions / len(ground_truth) if ground_truth else 0
    return accuracy


# Modified main function
def main():
    st.title("Face Recognition Attendance System with Accuracy Evaluation")

    # Initialize session state for attendance records
    if "attendance_df" not in st.session_state:
        st.session_state.attendance_df = pd.DataFrame(columns=["Name", "Time"])
    if "predictions" not in st.session_state:
        st.session_state.predictions = []
    if "ground_truth" not in st.session_state:
        st.session_state.ground_truth = []

    known_faces_folder = "facesData"
    known_face_encodings, known_face_names = load_known_faces(known_faces_folder)

    # Sidebar navigation
    page = st.sidebar.selectbox("Select a page",
                                ["Upload Photos", "Capture Image", "View Attendance Record", "Evaluate Accuracy"])

    if page == "Upload Photos":
        st.header("Upload Photos")
        uploaded_files = st.file_uploader("Choose images...", type=["jpg", "png"], accept_multiple_files=True)

        if uploaded_files:
            for uploaded_file in uploaded_files:
                st.write(f"Processing {uploaded_file.name}...")
                image = Image.open(uploaded_file)
                image = np.array(image)

                # Get ground-truth label from user input
                ground_truth_label = st.text_input(f"Enter the ground-truth name for {uploaded_file.name}:")
                if ground_truth_label:
                    st.session_state.ground_truth.append(ground_truth_label)
                    # Process the image and log predictions
                    process_image(image, st.session_state.attendance_df, known_face_encodings, known_face_names)
                    st.session_state.predictions.append(ground_truth_label)

    elif page == "Capture Image":
        st.header("Capture Image from Webcam")
        run = st.checkbox('Run Webcam')

        # Open webcam feed
        frame_window = st.image([])

        camera = cv2.VideoCapture(0)

        while run:
            ret, frame = camera.read()
            frame_window.image(frame, channels="BGR")

            # Capture frame when button is pressed
            if st.button("Capture Image"):
                process_image(frame, st.session_state.attendance_df, known_face_encodings, known_face_names)
                break

        camera.release()

    elif page == "View Attendance Record":
        st.header("Attendance Record")
        if st.session_state.attendance_df.empty:
            st.write("No attendance records found.")
        else:
            st.dataframe(st.session_state.attendance_df)

    elif page == "Evaluate Accuracy":
        st.header("Evaluate Model Accuracy")
        if not st.session_state.ground_truth:
            st.warning("No ground truth or predictions available for evaluation.")
        else:
            accuracy = evaluate_accuracy(st.session_state.predictions, st.session_state.ground_truth)
            st.success(f"Model Accuracy: {accuracy:.2f}")



if __name__ == "__main__":
    main()