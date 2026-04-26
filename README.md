# AI Classroom Analytics

An AI-powered application designed to detect and rate student engagement in a classroom environment using computer vision and machine learning. The project combines real-time face detection, an interactive dashboard, and extensive ML model tracking using MLflow.

## 🚀 Key Features

* **Real-time Face Detection:** Utilizes OpenCV and Haar Cascades via your webcam to count students in real-time.
* **Engagement Analytics Algorithm:** Calculates live engagement scores based on student presence.
* **Backend API & Analytics Server:** A lightweight Flask API protected by API key verification for internal data streaming.
* **Machine Learning & MLOps setup:** Standard experiment tracking built-in using Scikit-Learn and the MLflow Tracking Server.
* **DevOps Ready:** Contains native Docker containerization and a Jenkins CI/CD pipeline.

## 📦 Tech Stack

- **Core & Backend:** Python, Flask 
- **Computer Vision:** OpenCV (cv2)
- **Data & Models:** Scikit-Learn, Numpy, Pandas, TensorFlow
- **MLOps:** MLflow
- **Containerization:** Docker
- **CI/CD:** Jenkins

## 💻 Installation & Setup

1. **Clone the project & Navigate to the directory:**
   ```bash
   cd ai-classroom-analytics
   ```

2. **Activate your environment:**
   ```bash
   # On Windows
   env\Scripts\activate
   ```

3. **Install the required libraries:**
   ```bash
   pip install -r requirements.txt
   ```

## ▶️ Running the Project

The application runs locally in multiple components. Open a separate terminal for each command.

### 1. Classroom Analytics (Main Webcam Demo)
This script directly interfaces with the local webcam for student tracking.
```bash
python model/classroom_analytics.py
```
*Note: A video window will pop up showing face detection bindings and the engagement score overlay. Press `q` to safely close the camera.*

### 2. Backend Analytics API
Start the Flask application server. (By default configured to run on `http://127.0.0.1:5001`).
```bash
# If encountering relative import errors from standard Python, use python module execution
python -m backend.app
```
Endpoints available:
- **`GET /health`**: Healthcheck endpoint
- **`GET /analytics`**: Fetches the detected analytics (Requires `x-api-key` in header)

### 3. MLflow Dashboard
View your saved Machine Learning logs and tracked parameter experiments.
```bash
mlflow ui --backend-store-uri ./mlruns
```
Open your browser and navigate to exactly: `http://127.0.0.1:5000`

### 4. Optional: Run the ML Training Component
If you are iterating over new classification models or parameter variations, use the training script to track your run metrics.
```bash
python model/train_model.py
```
*Metrics are seamlessly integrated back into the MLflow UI.*

## 🔒 Security
The API integrates a basic authorization process (`security/auth.py`). Make sure to populate correct secrets into the backend server before connecting the frontend clients.
