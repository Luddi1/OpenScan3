from enum import Enum
import io
from tempfile import TemporaryFile
import time
from typing import IO

from libcamera import ColorSpace
ColorSpace.Jpeg = ColorSpace.Sycc
from picamera2 import Picamera2

from app.controllers.cameras.camera import CameraController
from app.models.camera import Camera, CameraMode

FOCUS_MIN = 0
FOCUS_MAX = 15
EXPOSURE_MIN = 1
EXPOSURE_MAX = 150

class Picamera2Camera(CameraController):
    __camera = [None, None] # [camera instance, mode]

    @classmethod
    def _get_camera(cls, camera: Camera, mode: CameraMode = None) -> Picamera2:
        if mode is None: # returning camera instance for focus, exposure, etc. settings
            pass
        elif cls.__camera[1] != mode:
            cls.__camera[1] = mode
            if cls.__camera[0]:
                cls.__camera[0].stop()
            else:
                cls.__camera[0] = Picamera2()
            if mode == CameraMode.PHOTO:
                cls.__camera[0].configure(cls.__camera[0].create_still_configuration())
            elif mode == CameraMode.PREVIEW:
                cls.__camera[0].configure(cls.__camera[0].create_preview_configuration(buffer_count=2,  main={"size": (640, 480)}))
            cls.__camera[0].start()

        return cls.__camera[0]

    @staticmethod
    def photo(camera: Camera) -> IO[bytes]:
        data = TemporaryFile()
        picam2 = Picamera2Camera._get_camera(camera, CameraMode.PHOTO)
        picam2.capture_file(data, format='jpeg')
        data.seek(0)
        return data

    @staticmethod
    def preview(camera: Camera) -> IO[bytes]:
        data = TemporaryFile()
        picam2 = Picamera2Camera._get_camera(camera, CameraMode.PREVIEW)
        picam2.capture_file(data, format='jpeg')
        data.seek(0)
        return data

    @staticmethod
    def set_focus(camera: Camera, auto_focus: bool, focus_val: int):
        # value range check
        if focus_val > FOCUS_MAX:
            focus_val = FOCUS_MAX
        elif focus_val < FOCUS_MIN:
            focus_val = FOCUS_MIN

        picam2 = Picamera2Camera._get_camera(camera)
        if picam2 is not None: # only works if started before
            if auto_focus:
                picam2.set_controls({"AfMode": 1})
            else:
                picam2.set_controls({"AfMode": 0, "LensPosition": focus_val})

    @staticmethod
    def set_exposure(camera: Camera, exposure_val: int):
        # value range check
        if exposure_val > EXPOSURE_MAX:
            exposure_val = EXPOSURE_MAX
        elif exposure_val < EXPOSURE_MIN:
            exposure_val = EXPOSURE_MIN

        # ms to us
        exposure_val = 1000 * exposure_val

        picam2 = Picamera2Camera._get_camera(camera)
        if picam2 is not None: # only works if started before
            picam2.set_controls({"ExposureTime": exposure_val, "AnalogueGain": 1.0})