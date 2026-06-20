from django.urls import path, include
from .views import (ProjectListCreateView, ProjectListView, ProjectDetailView,ProjectDeleteView,ProjectUpdateView)

urlpatterns = [
    path('create/', ProjectListCreateView.as_view(), name='create_project'),
    path('list/', ProjectListView.as_view(), name='list_projects'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='detail_project'),
    path('<int:pk>/update/', ProjectUpdateView.as_view(), name='update_project'),
    path('<int:pk>/delete/', ProjectDeleteView.as_view(), name='delete_project')
]