from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING, Optional

from django.db import IntegrityError

from robots.business_logic.exceptions import (
    RobotDoesNotExistsError,
    RobotModelAlreadyExistsError,
    RobotModelDoesNotExistsError,
)
from robots.models import Robot, RobotModel

if TYPE_CHECKING:
    from robots.business_logic.dto import RobotDTO


logger = getLogger(__name__)


def get_robots() -> list[Robot]:
    """
    Getting a list of all available robots in stock.
    """
    robots = Robot.objects.select_related('model').all()
    return list(robots)


def get_robot_by_id(id: int) -> Optional[Robot]:
    """
    Getting a robot by its ID.
    """
    try:
        robot: Robot = Robot.objects.select_related('model').get(pk=id)
    except Robot.DoesNotExist:
        logger.error('Robot does not exists.', extra={'robot_id': id})
        raise RobotDoesNotExistsError('This robot does not exists.')
    logger.info('Get robot successfully.', extra={'robot_id': id})
    return robot


def get_robot_models() -> list[RobotModel]:
    """
    Getting a list of all available models in stock.
    """
    robot_models = RobotModel.objects.all()
    return list(robot_models)


def get_robot_model_by_id(id: int) -> Optional[RobotModel]:
    """
    Getting a robots model by its ID.
    """
    try:
        robot_model: RobotModel = RobotModel.objects.get(pk=id)
    except RobotModel.DoesNotExist:
        logger.error('Model does not exists.', extra={'model_id': id})
        raise RobotModelDoesNotExistsError('This model does not exists. Register this model first.')
    logger.info('Get model successfully.', extra={'model_id': id})
    return robot_model


def get_robot_model_by_name(name: str) -> Optional[RobotModel]:
    """
    Getting a robots model by its name.
    """
    try:
        robot_model: RobotModel = RobotModel.objects.get(name=name)
    except RobotModel.DoesNotExist:
        logger.error('Model does not exists.', extra={'model_name': name})
        raise RobotModelDoesNotExistsError(f'Model {name} does not exists. Register this model first.')
    logger.info('Get model successfully.', extra={'model_name': name})
    return robot_model


def create_robot_model(name: str) -> Optional[RobotModel]:
    """
    Adding a new robot model. The model name must be unique.
    """
    try:
        robot_model: RobotModel = RobotModel.objects.create(name=name)
    except IntegrityError:
        logger.error('Model already exists.', extra={'model_name': name})
        raise RobotModelAlreadyExistsError(f'Model {name} already exists.')
    logger.info('Model created successfully', extra={'model_name': name})
    return robot_model


def create_robot(data: RobotDTO) -> Optional[Robot]:
    """
    Creating a new robot. First, there's a check for the presence of its model in the list of models.
    """
    model = get_robot_model_by_name(name=data.model)
    robot: Robot = Robot.objects.create(model=model, version=data.version, created=data.created)
    logger.info('Robot create successfully.', extra={'model': data.model, 'version': data.version})
    return robot
