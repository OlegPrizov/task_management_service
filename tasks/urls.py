from django.urls import path
from .views import task_list, task_create, task_detail, task_update

app_name = 'tasks'

urlpatterns = [
    path('', task_list, name='list'),
    path('create/', task_create, name='create'),
    path('<int:pk>/', task_detail, name='detail'),
    path('<int:pk>/edit/', task_update, name='edit'),
]