from __future__ import annotations

import json
from typing import TYPE_CHECKING

from django.http import JsonResponse
from django.views import View
from pydantic import ValidationError

from robots.business_logic.dto import RobotDTO
from robots.business_logic.exceptions import RobotModelDoesNotExistsError
from robots.business_logic.services import create_robot
from robots.presentation.common import convert_data_from_request_to_dto
from robots.presentation.rest_api_v1.serializers import CreateRobotSerializer

if TYPE_CHECKING:
    from django.http import HttpRequest
    from django.urls.exceptions import Resolver404


class CreateRobotApiView(View):
    """
    "REST API endpoint for creating a new entry in Robots.
    Accepts JSON input data and returns a JSON response."
    """

    def post(self, request: HttpRequest) -> JsonResponse:
        data = json.loads(request.body)
        try:
            CreateRobotSerializer(**data)
        except ValidationError as e:
            return JsonResponse({'message': str(e)}, status=400)
        data = convert_data_from_request_to_dto(dto=RobotDTO, data_from_request=data)
        try:
            create_robot(data=data)
            return JsonResponse({'message': 'Robot created successfully'}, status=201)
        except RobotModelDoesNotExistsError as e:
            return JsonResponse({'message': str(e)}, status=404)


def handle_not_found(request: HttpRequest, exception: Resolver404) -> JsonResponse:
    response_data = {'error': 'Not Found', 'message': 'The requested resource was not found.'}
    return JsonResponse(response_data, status=404)
