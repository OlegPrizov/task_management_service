from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from django.contrib.auth.decorators import login_required
from django.db.models import Q


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

    return render(request, 'tasks/task_form.html', {'form': form, 'button_text': 'Создать задачу',})

@login_required
def task_detail(request, pk):
    task = get_object_or_404(
    Task.objects.filter(Q(executor=request.user) | Q(creator=request.user)),
    pk=pk,
)
    return render(request, 'tasks/task_detail.html', {'task': task})

@login_required
def task_update(request, pk):
    task = get_object_or_404(
    Task.objects.filter(Q(executor=request.user) | Q(creator=request.user)),
    pk=pk,
)

    if request.method == 'POST':
        form = TaskCreateForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks:detail', pk=task.pk)
    else:
        form = TaskCreateForm(instance=task)

    return render(request, 'tasks/task_form.html', {
        'form': form,
        'task': task,
        'page_title': 'Редактирование задачи',
        'button_text': 'Сохранить изменения',
    })