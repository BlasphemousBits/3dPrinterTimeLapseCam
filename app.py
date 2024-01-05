from flask import Flask, render_template, Response
from flask_cors import CORS
import io
import serial
from rpi_camera import RpiCamera


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

camera = RpiCamera()

# serial_port = serial.Serial("/dev/ttyACM0", 9600)  # Replace with your serial port
# serial_data = b""

def gen_frames():
    
    while True:
        frame = camera.capture_frame()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
   
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':  
   app.run(host='0.0.0.0', port=5000, debug=True)
    