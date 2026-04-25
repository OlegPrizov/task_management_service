from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.project_list, name='list'),
    path("create/", views.ProjectCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", views.ProjectUpdateView.as_view(), name="edit"),
]