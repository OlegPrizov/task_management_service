from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'creator', 'executor', 'project', 'due_date')
    list_filter = ('status',)
    search_fields = ('title',)
