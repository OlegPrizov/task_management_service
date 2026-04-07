from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, Comment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import TaskCreateForm, CommentCreateForm
from projects.models import Project


def task_list(request):
    if not request.user.is_authenticated:
        return render(request, 'tasks/task_list.html', {
            'is_guest': True,
        })

    tasks = Task.objects.filter(
        Q(executor=request.user) | Q(creator=request.user)
    ).select_related(
        'creator',
        'executor',
        'project',
    ).distinct()

    user_projects = Project.objects.filter(
        Q(tasks__executor=request.user) | Q(tasks__creator=request.user)
    ).distinct().order_by('name')

    selected_project_id = request.GET.get('project')

    if selected_project_id:
        tasks = tasks.filter(project_id=selected_project_id)

    context = {
        'is_guest': False,
        'projects': user_projects,
        'selected_project_id': selected_project_id,
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
        Task.objects.select_related('creator', 'executor', 'project').prefetch_related('comments__user'),
        Q(pk=pk) & (Q(executor=request.user) | Q(creator=request.user))
    )

    if request.method == 'POST':
        comment_form = CommentCreateForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.task = task
            comment.user = request.user
            comment.save()
            return redirect('tasks:detail', pk=task.pk)
    else:
        comment_form = CommentCreateForm()

    return render(request, 'tasks/task_detail.html', {
        'task': task,
        'comment_form': comment_form,
    })

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

@login_required
def comment_update(request, task_pk, comment_pk):
    task = get_object_or_404(
        Task.objects.filter(Q(executor=request.user) | Q(creator=request.user)),
        pk=task_pk,
    )

    comment = get_object_or_404(
        Comment,
        pk=comment_pk,
        task=task,
        user=request.user,
    )

    if request.method == 'POST':
        form = CommentCreateForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Комментарий обновлён.')
            return redirect('tasks:detail', pk=task.pk)
    else:
        form = CommentCreateForm(instance=comment)

    return render(request, 'tasks/comment_form.html', {
        'task': task,
        'form': form,
        'page_title': 'Редактирование комментария',
        'button_text': 'Сохранить изменения',
    })


@login_required
def comment_delete(request, task_pk, comment_pk):
    task = get_object_or_404(
        Task.objects.filter(Q(executor=request.user) | Q(creator=request.user)),
        pk=task_pk,
    )

    comment = get_object_or_404(
        Comment,
        pk=comment_pk,
        task=task,
        user=request.user,
    )

    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Комментарий удалён.')
        return redirect('tasks:detail', pk=task.pk)

    return render(request, 'tasks/comment_confirm_delete.html', {
        'task': task,
        'comment': comment,
    })