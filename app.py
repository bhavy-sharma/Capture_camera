from flask import Flask, render_template, Response
import cv2
import threading

app = Flask(__name__)
video_capture = cv2.VideoCapture(0)  # Use 0 for default webcam

def generate_frames():
    while True:
        success, frame = video_capture.read()
        if not success:
            print("Failed to capture video.")
            break

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 5000}).start()
