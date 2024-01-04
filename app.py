from flask import Flask, render_template, Response
from flask_cors import CORS, cross_origin
from picamera2 import Picamera2
from picamera2.outputs import FileOutput 
from picamera2.encoders import MJPEGEncoder, JpegEncoder
import io
import serial
from threading import Condition

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

camera = Picamera2()
config = camera.create_video_configuration(main={"size": (1536, 864)}, raw=camera.sensor_modes[1])
camera.configure(config)
camera.start()

# serial_port = serial.Serial("/dev/ttyACM0", 9600)  # Replace with your serial port
# serial_data = b""

class StreamingOutput(io.BufferedIOBase):
	def __init__(self):
		self.frame = None
		self.condition = Condition()

	def write(self, buf):
		with self.condition:
			self.frame = buf
			self.condition.notify_all()
		

def gen_frames():
    output = StreamingOutput()
    camera.start_recording(JpegEncoder(), FileOutput(output))
    
    while True:
        with output.condition:
            output.condition.wait()
            frame = output.frame
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
    