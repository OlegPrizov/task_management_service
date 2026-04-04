from django.urls import path
from .views import task_list, task_create

app_name = 'tasks'

urlpatterns = [
    path('', task_list, name='list'),
    path('create/', task_create, name='create'),
]