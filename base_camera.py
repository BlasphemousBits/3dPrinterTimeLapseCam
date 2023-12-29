# base_camera.py

from abc import ABC, abstractmethod

class BaseCamera(ABC):
    """
    Abstract base class for cameras.

    This class provides a common interface for capturing frames from different
    types of cameras. Subclasses must implement the `capture_frame` method.
    """

    @abstractmethod
    def capture_frame(self):
        pass
