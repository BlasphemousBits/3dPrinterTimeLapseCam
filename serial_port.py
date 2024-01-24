import os
import logging
import threading
from datetime import datetime
from pathlib import Path
from queue import Queue
import serial

class SerialPort:
    BASE_SUBDIR = "timelapses"

    def __init__(self):
        try:
            self.serial_port = serial.Serial("/dev/ttyACM0", 9600)  # Replace with your serial port
        except serial.SerialException as e:
            logging.error("Error opening serial port: %s", e)
            raise

        self.base_path = Path('.') / self.BASE_SUBDIR
        try:
            os.makedirs(self.base_path, exist_ok=True)
        except OSError as e:
            logging.error("Error creating directory: %s", e)
            raise
        
        
    def read(self, queue):
        while True:
            data = self.serial_port.readline().decode().strip()
            queue.put(data)


    def monitor(self, take_picture, make_video):
        is_recording = False
        i = 0
        queue = Queue()
        # queue.put("Start:Shape-Box")
        # queue.put("// Cheese!")
        # queue.put("// Cheese!")
        serial_thread = threading.Thread(target=self.read, args=(queue,))
        serial_thread.daemon = True
        serial_thread.start()
        try:
            while True:
                data = queue.get()
                logging.info("from Printer: %s", data)
                if 'Start:' in data:
                    self.model_name = data.split(':')[1]
                    self.start_time = datetime.now().strftime("%y%m%d-%H%M")
                    self.filepath = self.base_path / f'{self.model_name}_{self.start_time}'
                    self.imagefilepath = self.filepath / 'images'
                    try:
                        os.makedirs(self.imagefilepath, exist_ok=True)
                    except OSError as e:
                        logging.error("Error creating directory: %s", e)
                        raise
                    
                    is_recording = True
                elif 'Stop:' in data:
                    is_recording = False
                    make_video(self.imagefilepath, f'{self.filepath}/{self.model_name}_{self.start_time}.mp4')
                    pass # Fill this out later
                elif data == "// Cheese!" and is_recording:
                    take_picture( f'{self.imagefilepath}/{i:06d}.jpg')
                    i += 1
        except KeyboardInterrupt:
            self.serial_port.close()
            
  
        
        