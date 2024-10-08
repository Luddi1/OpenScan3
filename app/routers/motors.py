from fastapi import APIRouter, Body

from app.controllers import motors
from app.models.motor import MotorType

router = APIRouter(
    prefix="/motors",
    tags=["motors"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_motors():
    return motors.get_motors()


@router.get("/{motor_type}")
async def get_motor(motor_type: MotorType):
    return motors.get_motor(motor_type)


@router.post("/{motor_type}/home")
async def move_motor(motor_type: MotorType):
    motor = motors.get_motor(motor_type)
    motors.home_motor(motor_type, motor)


@router.post("/{motor_type}/move_to")
async def move_motor(motor_type: MotorType, degrees: float):
    motor = motors.get_motor(motor_type)
    motors.move_motor_to(motor, degrees)


@router.post("/{motor_type}/move")
async def move_motor(motor_type: MotorType, degrees: float):
    motor = motors.get_motor(motor_type)
    motors.move_motor_degrees(motor, degrees)
