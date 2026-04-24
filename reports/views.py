from users.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from tasks.models import Task


@login_required
def reports_view(request):
    users = User.objects.all()

    report_data = []

    for user in users:
        tasks = Task.objects.filter(executor=user)

        total = tasks.count()
        todo = tasks.filter(status=Task.Status.TODO).count()
        in_progress = tasks.filter(status=Task.Status.IN_PROGRESS).count()
        completed = tasks.filter(status=Task.Status.DONE).count()

        overdue = tasks.filter(
            due_date__lt=timezone.now(),
            status__in=[
                Task.Status.TODO,
                Task.Status.IN_PROGRESS,
            ]
        ).count()

        report_data.append({
            "user": user,
            "total": total,
            "todo": todo,
            "in_progress": in_progress,
            "completed": completed,
            "overdue": overdue,
        })

    return render(request, "reports/reports.html", {
        "report_data": report_data
    })