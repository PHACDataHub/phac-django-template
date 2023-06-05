from django.contrib import messages
from django.db import transaction
from django.db.models.query import QuerySet
from django.forms.models import ModelForm
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from proj.rules_framework import test_rule
from proj.text import tdt

from my_app.models import Project, ProjectUserRole
from my_app.queries import get_project_qs_for_user

from .project_crud import *


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description", "project_type", "tags"]


class CreateProject(CreateView):
    form_class = ProjectForm
    model = Project
    template_name = "create_project.html"

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save()
            ProjectUserRole.objects.create(
                project=self.object,
                user=self.request.user,
                role=ProjectUserRole.LEADER_ROLE,
            )
            messages.add_message(
                self.request, messages.SUCCESS, tdt("Project created")
            )
            return super().form_valid(form)

    def get_success_url(self):
        return reverse("edit-project", args=[self.object.id])


class EditProject(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "edit_project.html"

    def get_success_url(self):
        # redirect to self
        return self.request.build_absolute_uri()


class ListProjects(ListView):
    def get_queryset(self):
        get_project_qs_for_user(self.request.user)
