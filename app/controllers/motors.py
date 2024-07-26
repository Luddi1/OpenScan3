import time
import math

from enum import Enum
from typing import Optional

from app.config import config
from app.config.motor import MotorConfig
from app.models.motor import Motor, MotorType

from app.controllers import gpio

def _sign(num):
    return -1 if num < 0 else 1

def get_motors() -> dict[MotorType, Motor]:
    return config.motors


def get_motor(motor_type: MotorType) -> Optional[Motor]:
    return config.motors.get(motor_type)

def home_motor(motor: Motor):
    if motor.settings.endstop_pin is None:
        return

    spr = motor.settings.steps_per_rotation
    dir = motor.settings.direction
    delay_init = motor.settings.delay
    delay = delay_init

    gpio.set_pin(motor.settings.direction_pin, dir)
    while (not gpio.read_input_pin(motor.settings.endstop_pin)):
        gpio.set_pin(motor.settings.step_pin, True)
        time.sleep(delay)
        gpio.set_pin(motor.settings.step_pin, False)
        time.sleep(delay)

    # moved to endstop, set degrees to predefined value
    motor.angle = motor.settings.endstop_angle
    motor.is_homed = True

def move_motor_to(motor: Motor, degrees: float):
    _sign(degrees) * (abs(degrees)%360)

    move_angles = degrees - motor.angle
    move_motor_degrees(motor, move_angles)


def move_motor_degrees(motor: Motor, degrees: float):
    spr = motor.settings.steps_per_rotation
    dir = motor.settings.direction
    ramp = motor.settings.acceleration_ramp
    acc = motor.settings.acceleration
    delay_init = motor.settings.delay
    delay = delay_init

    # check if within bounds
    if motor.is_homed:
        if (motor.angle + degrees) > motor.settings.endstop_angle:
            return # todo: throw error or exception
        if (motor.angle - degrees) < motor.settings.max_angle:
            return # todo: throw error or exception

    step_count = int(degrees * spr / 360) * dir

    if step_count > 0:
        gpio.set_pin(motor.settings.direction_pin, True)
    if step_count < 0:
        gpio.set_pin(motor.settings.direction_pin, False)
        step_count = -step_count
    for x in range(step_count):
        gpio.set_pin(motor.settings.step_pin, True)
        if x <= ramp and x <= step_count / 2:
            delay = delay_init * (
                1 + -1 / acc * math.cos(1 * (ramp - x) / ramp) + 1 / acc
            )
        elif step_count - x <= ramp and x > step_count / 2:
            delay = delay_init * (
                1 - 1 / acc * math.cos(1 * (ramp + x - step_count) / ramp) + 1 / acc
            )
        else:
            delay = delay_init
        time.sleep(delay)
        gpio.set_pin(motor.settings.step_pin, False)
        time.sleep(delay)

    motor.angle = motor.angle + degrees
    motor.angle = _sign(motor.angle) * (abs(motor.angle)%360)

