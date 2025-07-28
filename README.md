# UniAttend: Face Recognition Attendance System

UniAttend is a modern, web-based application designed to streamline the attendance process using facial recognition. Built with Flask and beautifully styled, it offers an intuitive and elegant solution for educational institutions and organizations to manage attendance seamlessly.

## ✨ Features

- **Elegant User Interface:** A clean, modern, and responsive UI with a university theme, built for a great user experience.
- **Dual Mode Operation:**
  - **Photo Upload:** Mark attendance by uploading images of attendees.
  - **Live Webcam Capture:** Use a webcam to capture images and mark attendance in real-time.
- **Persistent Attendance Records:** Attendance is saved to a CSV file, ensuring that records are maintained across sessions.
- **Facial Recognition:** Powered by the `face_recognition` library to accurately identify and verify individuals.

## 🛠️ Technologies Used

- **Backend:** Flask
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Core Library:** `face_recognition` (built on dlib)
- **Image Processing:** OpenCV, Pillow
- **Data Handling:** Pandas, NumPy

## 🚀 Setup and Installation

To get UniAttend up and running on your local machine, follow these simple steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/sakshikarande26/attendanceWithFaceRecognition.git
    cd attendanceWithFaceRecognition
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    python app.py
    ```

5.  Open your browser and navigate to `http://127.0.0.1:5000` to start using the application.

## Usage

- **Upload an Image:** Click on the "Choose File" button, select an image, and click "Upload & Recognize" to mark attendance.
- **Use Webcam:** Click on the "Capture & Recognize" button to use your webcam to capture a photo and mark attendance.
- **View Attendance:** Navigate to the "View Attendance" page to see all the recorded attendance logs.

## 🖼️ Screenshots

<img width="2851" height="1672" alt="output" src="https://github.com/user-attachments/assets/51d70538-1d98-42ba-9869-2309d4332fd9" />


---

*This project was developed to provide a simple yet powerful solution for attendance management. We hope you find it useful!*
