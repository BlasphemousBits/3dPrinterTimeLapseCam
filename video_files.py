from pathlib import Path

class Video:
    BASE_SUBDIR = "timelapses"
    def __init__(self, path: Path):
        self.base_path = Path('.') / self.BASE_SUBDIR
        self.path = path
        self.name = path.name
        self.video_path = self.path / f'{path.name}.mp4'
        self.image_path = self.path / "images"
        
    def has_video(self):
        return self.video_path.exists()

    def has_images(self):
        return self.image_path.exists() and self.image_path.is_dir()
        
    def get_video(self):
        return self.video_path
    
    def get_images(self):
        return self.image_path
    
class VideoFiles:
    BASE_SUBDIR = "timelapses"
    def __init__(self, path: Path):
        self.video_list=[]
        self.base_path = Path('.') / self.BASE_SUBDIR
        self.path = path
        self.name = path.name
        self.video_path = self.path / f'{path.name}.mp4'
        self.image_path = self.path / "images"
        
    def __iter__(self):
        return iter(self.video_list)