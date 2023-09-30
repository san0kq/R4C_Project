from pydantic import BaseModel


class CreateRobotSerializer(BaseModel):
    model: str
    version: str
    created: str
