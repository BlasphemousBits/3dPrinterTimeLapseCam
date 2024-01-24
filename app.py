from flask import Flask, render_template, Response, request, send_file, send_from_directory
from flask_cors import CORS
from rpi_camera import RpiCamera
import threading
import logging
from serial_port import SerialPort
from pathlib import Path
from video_files import Video

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

camera = RpiCamera()
serialport = SerialPort()

# serial_data = b""
logging.basicConfig(level=logging.DEBUG, handlers=[logging.FileHandler("logfile.txt"), logging.StreamHandler()])

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

@app.route('/files')
def display_files():
    directory_path = Path('timelapses')
    directory = map(Video, directory_path.iterdir())
    return render_template('files.html', directory = directory)
        
@app.route('/download_video/')
def download_video():
    filename = Path('timelapses') / request.args['file']
    return send_file(filename, as_attachment=True)
    
    

logging.debug("Starting monitor serial thread")
monitor_serial_thread = threading.Thread(target=serialport.monitor, args=(camera.capture_still_image, camera.make_video, ))
monitor_serial_thread.daemon = True
monitor_serial_thread.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)