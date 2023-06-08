from typing import Any

from django import http
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm, ModelForm
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from proj.form_util import BootstrapMixin
from proj.rules_framework import test_rule
from proj.text import tdt

from my_app.models import Project, ProjectUserRole
from my_app.queries import get_project_qs_for_user

from .project_crud import *


class ProjectForm(ModelForm, BootstrapMixin):
    class Meta:
        model = Project
        fields = [
            "name_en",
            "name_fr",
            "description_en",
            "description_fr",
            "project_type",
            "tags",
        ]


class CreateProject(CreateView):
    form_class = ProjectForm
    model = Project
    template_name = "create_project.jinja2"

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
        return reverse("edit_project", args=[self.object.id])


class EditProject(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "edit_project.jinja2"

    def form_valid(self, form):
        ret = super().form_valid(form)
        messages.add_message(
            self.request, messages.SUCCESS, tdt("Project updated")
        )
        return ret

    def get_success_url(self):
        # redirect to self
        return self.request.build_absolute_uri()

    def dispatch(self, request, *args: Any, **kwargs) -> HttpResponse:
        if not test_rule(
            "can_modify_project", self.request.user, self.kwargs.get("pk")
        ):
            raise PermissionDenied(tdt("You can't view this project"))

        return super().dispatch(request, *args, **kwargs)


class ListProjects(ListView):
    template_name = "list_projects.jinja2"

    def get_queryset(self):
        return get_project_qs_for_user(self.request.user)


class ProjectPreviewModal(DetailView):
    model = Project
    template_name = "project_preview_modal.jinja2"

    def dispatch(self, request, *args, **kwargs):
        if not test_rule(
            "can_view_project", self.request.user, self.kwargs.get("pk")
        ):
            raise PermissionDenied(tdt("You can't view this project"))

        resp = super().dispatch(request, *args, **kwargs)
        # add header
        resp["HX-Trigger-After-Settle"] = "activate-modal"
        return resp
