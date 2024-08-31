from dataclasses import dataclass


@dataclass
class MotorConfig:
    direction_pin: int
    enable_pin: int
    step_pin: int
    endstop_pin: int

    acceleration: int
    acceleration_ramp: int
    delay: int
    direction: int # 1 or -1
    steps_per_rotation: int
    endstop_angle: float
    max_angle: float # furthest away from endstop
