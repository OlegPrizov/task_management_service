from django import forms
from .models import Task, Comment


class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'status', 'executor', 'watchers', 'project']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Введите название задачи'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Описание задачи'}),
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'watchers': forms.CheckboxSelectMultiple(),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user:
            self.fields['watchers'].queryset = self.fields['watchers'].queryset.exclude(pk=self.user.pk)

    def clean(self):
        cleaned_data = super().clean()
        executor = cleaned_data.get('executor')
        watchers = cleaned_data.get('watchers')

        if not watchers:
            return cleaned_data

        if self.user and self.user in watchers:
            self.add_error('watchers', 'Постановщик задачи не может быть наблюдателем.')

        if executor and executor in watchers:
            self.add_error('watchers', 'Исполнитель задачи не может быть наблюдателем.')

        return cleaned_data

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