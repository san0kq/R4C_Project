from dataclasses import dataclass


@dataclass
class RobotDTO:
    model: str
    version: str
    created: str
