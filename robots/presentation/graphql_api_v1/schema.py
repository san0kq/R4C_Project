from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

import graphene
from graphene_django import DjangoObjectType

from robots.business_logic.dto import RobotDTO
from robots.business_logic.services import (
    create_robot,
    create_robot_model,
    get_robot_by_id,
    get_robot_model_by_id,
    get_robot_model_by_name,
    get_robot_models,
    get_robots,
)
from robots.models import Robot, RobotModel

if TYPE_CHECKING:
    from graphene import ObjectType, ResolveInfo


class RobotModelType(DjangoObjectType):
    class Meta:
        model = RobotModel


class RobotType(DjangoObjectType):
    class Meta:
        model = Robot


class RobotModelInput(graphene.InputObjectType):
    name = graphene.String()


class RobotInput(graphene.InputObjectType):
    model = graphene.Field(RobotModelInput)
    version = graphene.String()
    created = graphene.DateTime()


class Query(graphene.ObjectType):
    robot = graphene.Field(RobotType, id=graphene.Int())
    robot_model = graphene.Field(RobotModelType, id=graphene.Int())
    robots = graphene.List(RobotType)
    robot_models = graphene.List(RobotModelType)

    def resolve_robot(self, info: ResolveInfo, **kwargs: Any) -> Optional[Robot]:
        id = kwargs.get('id')

        if id is not None:
            robot = get_robot_by_id(id=id)
            return robot

        return None

    def resolve_robot_model(self, info: ResolveInfo, **kwargs: Any) -> Optional[RobotModel]:
        id = kwargs.get('id')

        if id is not None:
            robot_model = get_robot_model_by_id(id=id)
            return robot_model

        return None

    def resolve_robots(self, info: ResolveInfo, **kwargs: Any) -> list[Robot]:
        robots = get_robots()
        return robots

    def resolve_robot_models(self, info: ResolveInfo, **kwargs: Any) -> list[RobotModel]:
        robot_models = get_robot_models()
        return robot_models


class CreateRobotModel(graphene.Mutation):
    class Arguments:
        input = RobotModelInput(required=True)

    ok = graphene.Boolean()
    robot_model = graphene.Field(RobotModelType)

    @staticmethod
    def mutate(
        root: ObjectType, info: ResolveInfo, input: Optional[RobotModelInput] = None
    ) -> Optional[CreateRobotModel]:
        ok = True
        if input:
            robot_model_instance = create_robot_model(name=input.name)
            return CreateRobotModel(ok=ok, robot_model=robot_model_instance)
        else:
            return None


class CreateRobot(graphene.Mutation):
    class Arguments:
        input = RobotInput(required=True)

    ok = graphene.Boolean()
    robot = graphene.Field(RobotType)

    @staticmethod
    def mutate(root: ObjectType, info: ResolveInfo, input: Optional[RobotInput] = None) -> Optional[CreateRobot]:
        ok = True
        if input:
            model = get_robot_model_by_name(name=input.model.name)
        else:
            return None
        if model is None:
            return CreateRobot(ok=False, robot=None)
        data = RobotDTO(model=model.name, version=input.version, created=input.created)
        robot_instance = create_robot(data=data)
        return CreateRobot(ok=ok, robot=robot_instance)


class Mutation(graphene.ObjectType):
    create_robot_model = CreateRobotModel.Field()
    create_robot = CreateRobot.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
