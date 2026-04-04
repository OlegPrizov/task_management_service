from django.shortcuts import render
from .models import Task
from django.contrib.auth.decorators import login_required


from django.shortcuts import render
from .models import Task
from users.models import User


def task_list(request):
    tasks = Task.objects.all()

    context = {
        'todo_tasks': tasks.filter(status=Task.Status.TODO),
        'in_progress_tasks': tasks.filter(status=Task.Status.IN_PROGRESS),
        'done_tasks': tasks.filter(status=Task.Status.DONE),
    }

    return render(request, 'tasks/task_list.html', context)

from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskCreateForm


def task_list(request):
    if not request.user.is_authenticated:
        return render(request, 'tasks/task_list.html', {
            'is_guest': True,
        })

    tasks = Task.objects.filter(executor=request.user).select_related(
        'creator',
        'executor',
        'project',
    )

    context = {
        'is_guest': False,
        'todo_tasks': tasks.filter(status=Task.Status.TODO),
        'in_progress_tasks': tasks.filter(status=Task.Status.IN_PROGRESS),
        'done_tasks': tasks.filter(status=Task.Status.DONE),
    }

    return render(request, 'tasks/task_list.html', context)

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.creator = request.user
            task.save()
            return redirect('tasks:list')
    else:
        form = TaskCreateForm()

    return render(request, 'tasks/task_form.html', {'form': form})