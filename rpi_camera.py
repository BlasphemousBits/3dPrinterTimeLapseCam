 # rpi_camera.py

import io
import picamera
from PIL import Image
from base_camera import BaseCamera

class RpiCamera(BaseCamera):
    def __init__(self, resolution=(640, 480)):
        self.camera_instance = picamera.PiCamera()
        self.camera_instance.resolution = resolution

    def capture_frame(self):
        frame_stream = io.BytesIO()
        self.camera_instance.capture(frame_stream, format='jpeg', use_video_port=True)
        frame_stream.seek(0)
        return Image.open(frame_stream)

    def capture_still_image(self):
        self.camera_instance.capture('still_image.jpg')
 