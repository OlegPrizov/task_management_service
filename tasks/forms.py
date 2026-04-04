from django import forms
from .models import Task


class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'status', 'executor', 'project']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Введите название задачи'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Описание задачи'}),
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }