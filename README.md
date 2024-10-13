# Face Recognition Attendance System

## Overview
The Face Recognition Attendance System is a web application developed using Streamlit that enables users to capture images through a webcam or upload photos. The system recognizes faces using deep learning and records attendance in real time. The application features a simple user interface that allows easy navigation and interaction.

## Key Components

1. **Face Recognition Library**:
   - Utilizes the `face_recognition` library, built on top of `dlib`, for detecting and recognizing faces from images.

2. **Image Processing**:
   - Captures and processes images either from the user's webcam or through uploaded files.
   - Converts images from BGR (OpenCV format) to RGB for compatibility with the face recognition library.

3. **Known Faces Dataset**:
   - Loads known face encodings and names from a specified directory (`facesData`), where each subfolder is named in the `name_surname` format.
   - Each subfolder contains 2-3 images of the corresponding person, which are used to generate facial encodings for recognition.

4. **Attendance Recording**:
   - Maintains an attendance DataFrame using `pandas`, which is stored in Streamlit's session state to ensure persistence across page reloads.
   - Marks attendance with the recognized person's name and the current timestamp when a match is found.

5. **Webcam Integration**:
   - Incorporates real-time webcam functionality using OpenCV, allowing users to capture images directly from their webcam.
   - The application displays a live video feed and processes the captured frame for face recognition.

6. **User Interface**:
   - Built with Streamlit, providing an intuitive layout with sidebar navigation to switch between functionalities (uploading photos, capturing images, and viewing attendance records).
   - Displays processed images along with face bounding boxes and recognized names.

7. **Attendance Display**:
   - Provides a dedicated page for viewing attendance records in a tabular format, allowing users to check marked attendance.

## Workflow

1. **Initialization**:
   - The application initializes by loading known face encodings and names from the `facesData` folder into memory.

2. **User Interaction**:
   - Users can navigate between different functionalities using the sidebar:
     - **Upload Photos**: Users can upload images for recognition.
     - **Capture Image**: Users can activate the webcam to capture a real-time image.
     - **View Attendance Record**: Displays the current attendance records in a DataFrame.

3. **Face Detection and Recognition**:
   - Upon uploading a photo or capturing an image, the application detects faces using `face_recognition` and compares the detected faces against the known encodings.
   - If a match is found, the corresponding name is recorded along with the timestamp.

4. **Attendance Management**:
   - The attendance records are stored in the session state, allowing users to view the records without losing any data when navigating between pages.

5. **Real-Time Feedback**:
   - Provides visual feedback during processing, displaying messages and images to inform users of the results.

## Potential Enhancements
- **Export Attendance Records**: Implement functionality to download attendance records as CSV files.
- **Notifications**: Add notification alerts for successful attendance marking.
- **Improved UI/UX**: Enhance the interface with better design and clearer instructions.
- **Performance Optimization**: Implement optimizations to reduce processing time and improve accuracy.

## Conclusion
The Face Recognition Attendance System effectively combines deep learning for face recognition with an easy-to-use web interface, providing a functional solution for attendance tracking. The use of Streamlit enables rapid development and deployment, making it accessible for users with varying levels of technical expertise.

## Installation
To set up and run the project, follow these steps:

1. Clone the repository:
   ```bash
   git clone <repository-url>
# attendanceWithFaceRecognition
