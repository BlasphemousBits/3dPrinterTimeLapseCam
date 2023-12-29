import threading
import time
from io import BytesIO

from PIL import Image, ImageDraw


class MockCamera:
    current_frame = None
    
    def __init__(self) -> None:
        #self.current_frame = self.create_test_image()
        self.thread = threading.Thread(target=self.camera_thread, daemon=True)
        self.thread.start()
        
    def camera_thread(self):
        frame_iter = self.get_frames()
        for frame in frame_iter:
            self.current_frame = frame
            time.sleep(0)
        
    def get_frames(self):
        img = Image.new("RGB", (800, 600), color="LightBlue")
        d = ImageDraw.Draw(img)
        while True:
            for i in range(10):
                d.rectangle([(0, 0), (800, 600)], fill="LightBlue")
                d.text(
                    (400, 300), text=str(i), fill="black", anchor="mm", font_size=100
                )
                img_io = BytesIO()
                img.save(img_io, "JPEG", quality=70)
                img_io.seek(0)
                yield img_io.read()
                time.sleep(.5)

    def next_frame(self):
        time.sleep(0)
        return self.current_frame

        