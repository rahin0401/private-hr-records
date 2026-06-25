from django.urls import path
from .views import DashboardStatsView,DownloadSyntheticDatasetView

urlpatterns= [
    path('stats/',DashboardStatsView.as_view(),name= "dashboard"),
    path('project/<int:pk>/download/',DownloadSyntheticDatasetView.as_view(),name = 'download_dataset'),
]

