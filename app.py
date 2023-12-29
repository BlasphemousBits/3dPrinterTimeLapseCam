from flask import Flask, render_template, Response
from flask_cors import CORS, cross_origin
from MockCamera import MockCamera

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

camera = MockCamera()

@app.route('/')
def home():
    return render_template('home.html')

def next_frame():
    yield b"--frame/r/n"
    while True:
        frame = camera.next_frame()
        yield b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n--frame\r\n"

@app.route('/video_feed')
def video_feed():
    response = Response(next_frame(), mimetype="multipart/x-mixed-replace; boundary=frame")

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    #return Response(next_frame(), mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == '__main__':  
   app.run()
    