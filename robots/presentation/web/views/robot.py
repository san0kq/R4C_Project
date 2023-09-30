from __future__ import annotations

from typing import TYPE_CHECKING

from django.http import HttpResponse
from django.views import View

from robots.business_logic.services import create_excel

if TYPE_CHECKING:
    from django.http import HttpRequest


class DownloadExcelView(View):
    """
    A Excel file is created in the controller, which contains information
    about the robots created in the last week, and this file is sent as a response."
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        create_excel()

        with open('robot_week.xlsx', 'rb') as excel_file:
            response = HttpResponse(excel_file.read(), content_type='application/ms-excel')
            response["Content-Disposition"] = 'attachment; filename="robot_week.xlsx"'
        return response
