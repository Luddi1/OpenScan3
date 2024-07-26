import RPi.GPIO as GPIO

from app.config import config

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

_pin_status = {}


def _initialize_output_pin(pin: int):
    _pin_status[pin] = False
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)


def _initialize_input_pin(pin: int):
    GPIO.setup(pin, GPIO.IN)


def _initialize_pins():
    for pin in [
        *config.ring_light_pins,
        *[motor.settings.direction_pin for motor in config.motors.values()],
        *[motor.settings.enable_pin for motor in config.motors.values()],
        *[motor.settings.step_pin for motor in config.motors.values()],
        config.external_camera_pin
    ]:
        _initialize_output_pin(pin)

    for pin in [
        *[motor.settings.endstop_pin for motor in config.motors.values() if motor.settings.endstop_pin is not None],
    ]:
        _initialize_input_pin(pin)

def toggle_pin(pin: int):
    set_pin(pin, not _pin_status[pin])


def set_pin(pin: int, status: bool):
    _pin_status[pin] = status
    GPIO.output(pin, status)


def get_pins():
    return _pin_status


def get_pin(pin: int):
    return _pin_status[pin]


def read_input_pin(pin: int):
    return GPIO.input(pin)


_initialize_pins()
