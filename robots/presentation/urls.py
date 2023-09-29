from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from robots.presentation.rest_api_v1.views import CreateRobotApiView

urlpatterns = [path('robot/', csrf_exempt(CreateRobotApiView.as_view()), name='robot')]
