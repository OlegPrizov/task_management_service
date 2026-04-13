from django.urls import path
from .views import (
    task_list,
    task_create,
    task_detail,
    task_update,
    comment_update,
    comment_delete,
    task_report_xlsx
)

app_name = 'tasks'

urlpatterns = [
    path('', task_list, name='list'),
    path('create/', task_create, name='create'),
    path('<int:pk>/', task_detail, name='detail'),
    path('<int:pk>/edit/', task_update, name='edit'),
    path('<int:task_pk>/comments/<int:comment_pk>/edit/', comment_update, name='comment_edit'),
    path('<int:task_pk>/comments/<int:comment_pk>/delete/', comment_delete, name='comment_delete'),
    path('<int:pk>/report/xlsx/', task_report_xlsx, name='report_xlsx'),
]