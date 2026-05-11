from django.urls import path
from . import views

app_name = "reports"

urlpatterns = [
    path('', views.reports_view, name="index"),
    path('executors/xlsx/', views.executors_report_xlsx, name="executors_xlsx"),
    path('projects/xlsx/', views.projects_report_xlsx, name="projects_xlsx"),
    path('departments/xlsx/', views.departments_report_xlsx, name="departments_xlsx"),
    path('workload/xlsx/', views.workload_report_xlsx, name="workload_xlsx"),
    path('priority/xlsx/', views.priority_report_xlsx, name="priority_xlsx"),
    path('velocity/xlsx/', views.velocity_report_xlsx, name="velocity_xlsx"),
    path('sla/xlsx/', views.sla_report_xlsx, name="sla_xlsx"),
]