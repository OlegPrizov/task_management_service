from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from .models import Project


from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.shortcuts import render

from .models import Project


@login_required
def project_list(request):
    projects = Project.objects.filter(
        Q(tasks__creator=request.user) |
        Q(tasks__executor=request.user)
    ).annotate(
        user_tasks_count=Count(
            'tasks',
            filter=Q(tasks__creator=request.user) |
                   Q(tasks__executor=request.user),
            distinct=True
        )
    ).distinct().order_by('-created_at')

    return render(request, 'projects/project_list.html', {
        'projects': projects
    })