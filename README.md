# AI Classroom Analytics

An AI-powered application designed to detect and rate student engagement in a classroom environment using computer vision and machine learning. 

This repository connects real-time video stream inferences, a local MLOps pipeline for tracking algorithm parameters, and a protected REST API for retrieving session-level metrics. It includes infrastructure scaffolds for CI/CD and Containerization.

---

## 🏗️ Project Architecture 

The application consists of distinct decoupled components. Here is an extremely detailed breakdown of every integrated part of the repository:

### 1. Computer Vision Runtime (`model/classroom_analytics.py`)
- **Backend Setup**: Initializes `cv2.VideoCapture(0, cv2.CAP_DSHOW)` (explicitly using the Windows DirectShow driver to prevent Media Foundation initialisation freezes).
- **Detection Algorithm**: Uses standard OpenCV face detection through a local Haar Cascade XML (`haarcascade_frontalface_default.xml`).
- **Processing**: Reads the frame, converts it to grayscale using `cv2.COLOR_BGR2GRAY`, and parses detection via `detectMultiScale` (configured with `scaleFactor=1.3` and `minNeighbors=5`).
- **UI Overlay**: Draws a standard green rectangle (`(0, 255, 0)`) of thickness `2` globally around detected coordinates `(x, y, w, h)`.
- **Metrics Algorithm**: Derives *Engagement Score* mapped at `min(student_count * 10, 100)`. Renders text with `cv2.FONT_HERSHEY_SIMPLEX`.
- **Exit Control**: Await key `q` using `cv2.waitKey(1) & 0xFF == ord('q')` to gracefully kill the window and release the CAP driver.

### 2. Backend Analytics Server (`backend/app.py`)
- **Framework**: Flask WSGI application mounted on module execution `python -m backend.app`.
- **Server Ports**: Explicitly binds to `host="0.0.0.0"` targeting `port=5001` (to prevent collision with MLflow running locally on port 5000).
- **Cross-Component Loading**: Appends root directory to `sys.path` to permit absolute `import security.auth`. 
- **Internal Routes**:
    - `GET /`: Simple text representation confirming server starts.
    - `GET /health`: Returns standard JSON `{"status": "running"}`.
    - `GET /analytics`: 
        1. **Security Hook**: Parses `x-api-key` from incoming HTTP headers. Evaluates against `auth.verify()`. Returns `401 Unauthorized` on failure.
        2. **Payload**: Currently generates a simulated payload of `random.randint(3,10)` for `students_present` and normalizes the `engagement_score`.

### 3. Identity Auth Engine (`security/auth.py`)
- **Verification Protocol**: Statically maintains an `API_KEY` mapped directly to `"classroom_secure_key"`. Exposes a `verify(key)` function to guard the Flask Routes.

### 4. MLOps Experiment Tracking (`model/train_model.py` & `mlruns/`)
- **Dataset**: Uses Scikit-Learn's Iris sample (`load_iris()`) for model bootstrapping, mapped via a 80/20 train/test split.
- **Underlying Model**: Trains a benchmark `LogisticRegression` classification model tracking baseline accuracy using test arrays.
- **MLflow Tracking API**: Uses `mlflow.start_run()` to trace configurations.
    - Logs parameter `model: LogisticRegression`.
    - Logs metric `accuracy`.
    - Automatically serializers and registers the binary classifier via `mlflow.sklearn.log_model(model, "model")`.
- **MLflow Store**: Utilizes local `mlruns/` schema storage directories combined with SQLite backend representations (`mlflow.db`) to preserve data states securely locally.

### 5. DevOps CI/CD & Deployments
- **Docker (`docker/Dockerfile`)**: Base python container utilizing `python:3.9` image. Handles working directories (`WORKDIR /app`), caches `requirements.txt` installs securely via pip, and automatically targets the REST Flask Server using `CMD ["python", "-m", "backend.app"]`.
- **Jenkins (`Jenkinsfile`)**: Contains natively scoped Jenkins stages. Explicitly includes three functional stages:
    1. `Install Dependencies`: Target placeholder.
    2. `Run Test`: Validates pipeline working logs.
    3. `Check Python`: Triggers a `.bat` execution invoking a local static interpreter `C:\Users\Dhrumil Patel\AppData\Local\Programs\Python\Python313\python.exe --version` to enforce execution stability mapping.

### 6. Sub-Directories & Configurations
- **Dependencies (`requirements.txt`)**: Strict configuration packages handling (`opencv-python`, `numpy`, `pandas`, `flask`, `mlflow`, `scikit-learn`). (*Note: TensorFlow was explicitly removed standardizations.*)
- **Runtime Constraints (`runtime.txt`)**: Locks Python compilation limits formally defined to `python-3.10.13`.
- **Data Stores**: Retains unpopulated scaffolding environments (`data/` and `experiments/`) intentionally to support iterative extraction endpoints.

---

## 💻 Setup Instructions

1. **Clone the Repository & Prepare Path**
   ```bash
   cd ai-classroom-analytics
   ```

2. **Initialize Environment Variables**
   Locate your executable and load virtual mappings.
   ```bash
   # Windows Environment Generation Executable
   env\Scripts\activate
   ```

3. **Install Package Requirements**
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Running The Applications

For proper execution, component environments should be isolated into standalone concurrent terminals.

### 1. OpenCV Classroom Detection Pipeline
```bash
python model/classroom_analytics.py
```
*Note: Due to explicit hardware ties, this must be executed in an iterative graphical terminal rather than background system services.*

### 2. Live Analytics REST API
```bash
python -m backend.app
```
Endpoints deploy successfully against `http://127.0.0.1:5001`. Ensure `x-api-key: classroom_secure_key` is passed globally during request headers.

### 3. Start MLflow MLOps Dashboard
```bash
mlflow ui --backend-store-uri ./mlruns
```
Host defaults to `http://127.0.0.1:5000`. Navigate to the web browser to access tracking statistics.
