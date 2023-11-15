import time
from flask import Flask, render_template, Response

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

imgs = [open(f + '.jpg', 'rb').read() for f in ['1', '2', '3']]

def get_frame():
    return imgs[int(time.time()) % 3]

def gen():
    yield b'--frame/r/n'
    while True:
        frame = get_frame()
        yield  b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n--frame\r\n'

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype="multipart/x-mixed-replace; boundary=frame")