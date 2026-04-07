from django import forms
from .models import Task, Comment


class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'status', 'executor', 'project']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Введите название задачи'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Описание задачи'}),
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': 'Напишите комментарий...'
                }
            ),
        }