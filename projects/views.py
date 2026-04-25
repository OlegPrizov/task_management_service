from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Project
from .forms import ProjectForm

@login_required
def project_list(request):
    projects = Project.objects.filter(
        Q(owner=request.user) |
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

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects/project_form.html"
    success_url = reverse_lazy("projects:list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects/project_form.html"
    success_url = reverse_lazy("projects:list")

    def test_func(self):
        project = self.get_object()
        return project.owner == self.request.user