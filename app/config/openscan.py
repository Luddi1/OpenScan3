import json
import pathlib
import os

from app.config.camera import CameraSettings
from app.config.cloud import CloudSettings
from app.config.motor import MotorConfig
from app.models.motor import Motor, MotorType

from dotenv import load_dotenv

class OpenScanConfig:
    def __init__(self):
        OpenScanConfig.reload()

    @classmethod
    def reload(cls):
        load_dotenv()
        # cls.scanner = ScannerConfig(turntable_mode=False)
        # cls.cloud = OpenScanCloudConfig("", "", "", "")
        cls.cameras: dict[str, CameraSettings] = OpenScanConfig._get_camera_configs()
        cls.motors: dict[str, Motor] = {
            # "tt": OpenScanConfig._load_motor_config("turntable"),
            # "rotor": OpenScanConfig._load_motor_config("rotor"),
            MotorType.TURNTABLE: Motor(MotorConfig(6, 22, 16, None, 1, 100, 0.0001, 1, 3200, 0, 0)),
            MotorType.ROTOR: Motor(MotorConfig(23, 22, 27, 17, 1, 2000, 0.0001, -1, 66000, -60, 90)),
        }
        cls.projects_path = pathlib.PurePath("projects")
        cls.cloud = CloudSettings(
            "openscan",
            "free",
            os.getenv("OPENSCANCLOUD_KEY"),
            "http://openscanfeedback.dnsuser.de:1334",
        )
        cls.ring_light_enabled = True
        cls.ring_light_pins = (24, 26)

        cls.external_camera_pin = 5
        cls.external_camera_delay = 0.1


    @staticmethod
    def _load_motor_config(name: str) -> MotorConfig:
        with open(f"settings/motor_{name}.json") as f:
            config = json.load(f)
            return MotorConfig(**config)

    @staticmethod
    def _load_camera_config(name: str) -> CameraSettings:
        return {}

    @staticmethod
    def _get_camera_configs() -> dict[str, CameraSettings]:
        return {}
