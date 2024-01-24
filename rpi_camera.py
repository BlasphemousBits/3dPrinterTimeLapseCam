 # rpi_camera.py
import io
from threading import Condition
from picamera2 import Picamera2
from picamera2.outputs import FileOutput 
from picamera2.encoders import  JpegEncoder
from libcamera import controls
from moviepy.editor import ImageSequenceClip
import logging

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
        self.camera.set_controls({"AfMode": controls.AfModeEnum.Manual, "LensPosition": 6})
        self.camera.start_recording(JpegEncoder(), FileOutput(self.output))

    def capture_frame(self):
         with self.output.condition:
            self.output.condition.wait()
            frame = self.output.frame
            return frame

    def capture_still_image(self, filename):
        # temp logging statement.
        logging.debug("capturing")
        self.camera.capture_file(filename)
    
    
    def make_video(self, imagefilepath, videofilepath):  
        video = ImageSequenceClip(imagefilepath, fps = 30)
        video.write_videofile(videofilepath, codec='libx264', ffmpeg_params=['-crf' ,'17', '-pix_fmt' ,'yuv420p'])
 