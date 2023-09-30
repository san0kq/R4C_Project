from django.urls import path

from robots.presentation.web.views import DownloadExcelView

urlpatterns = [path('download-excel', DownloadExcelView.as_view(), name='download-excel')]
