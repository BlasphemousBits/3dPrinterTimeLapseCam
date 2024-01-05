 # rpi_camera.py

import io
from threading import Condition
from picamera2 import Picamera2
from picamera2.outputs import FileOutput 
from picamera2.encoders import  JpegEncoder

class StreamingOutput(io.BufferedIOBase):
	def __init__(self):
		self.frame = None
		self.condition = Condition()

	def write(self, buf):
		with self.condition:
			self.frame = buf
			self.condition.notify_all()

class RpiCamera():
    def __init__(self):
        self.camera = Picamera2()
        config = self.camera.create_video_configuration(main={"size": (1536, 864)}, raw=self.camera.sensor_modes[1])
        self.camera.configure(config)
        self.camera.start()
        self.output = StreamingOutput()
        self.camera.start_recording(JpegEncoder(), FileOutput(self.output))

    def capture_frame(self):
         with self.output.condition:
            self.output.condition.wait()
            frame = self.output.frame
            return frame

    def capture_still_image(self):
        self.camera_instance.capture('still_image.jpg')
 