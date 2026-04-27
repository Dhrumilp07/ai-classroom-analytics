import cv2
import requests
import threading
# Load face detection model
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

frame_counter = 0

def update_backend(students, engagement):
    try:
        requests.post("http://127.0.0.1:5001/update_analytics",
                      json={"students_present": students, "engagement_score": engagement},
                      headers={"x-api-key": "classroom_secure_key"},
                      timeout=1)
    except:
        pass

while True:
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5
    )

    student_count = len(faces)

    # Draw rectangles around faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

    # Engagement score
    engagement = min(student_count * 10, 100)

    # Send live data to backend asynchronously every 5 frames to prevent freezing
    frame_counter += 1
    if frame_counter % 5 == 0:
        threading.Thread(target=update_backend, args=(student_count, engagement), daemon=True).start()

    cv2.putText(frame,
                f"Students: {student_count}",
                (10,30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,255,0),
                2)

    cv2.putText(frame,
                f"Engagement: {engagement}%",
                (10,70),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,255,0),
                2)

    cv2.imshow("AI Classroom Analytics", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()