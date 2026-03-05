from django.urls import reverse

import htpy as h

from proj.htpy.base_page import BasePageTemplate
from proj.htpy.generic_form import GenericForm
from proj.htpy.modal_base import ModalBaseTemplate
from proj.text import tdt


class ListProjectsPage(BasePageTemplate):
    def content(self):
        return [
            h.h1[tdt("Project list")],
            h.a(href=reverse("create_project"))[tdt("Create new project")],
            h.ul[
                [
                    h.li[
                        h.a(
                            hx_select_oob="#modal-mount-point",
                            hx_swap="none",
                            hx_get=reverse(
                                "preview_project_modal", args=[project.id]
                            ),
                            href="#",
                        )[project.name],
                    ]
                    for project in self.context["object_list"]
                ]
            ],
        ]


class CreateProjectPage(BasePageTemplate):

    def content(self):
        from django.middleware.csrf import get_token

        return [
            h.h1[tdt("Create project")],
            h.a(href=reverse("list_projects"), class_="btn btn-warning")[
                tdt("Cancel")
            ],
            h.form(method="post", novalidate=True)[
                GenericForm(
                    self.context["form"], get_token(self.request)
                ).render(),
                h.div(".text-end")[
                    h.input(
                        ".btn.btn-success.btn-lg",
                        type="submit",
                        value=tdt("Create"),
                    ),
                ],
            ],
        ]


class EditProjectPage(BasePageTemplate):

    def content(self):
        from django.middleware.csrf import get_token

        return [
            h.h1[tdt("Edit project"), " : ", self.context["object"].name],
            h.a(href=reverse("list_projects"), class_="btn btn-warning")[
                tdt("Cancel")
            ],
            h.form(method="post")[
                GenericForm(
                    self.context["form"], get_token(self.request)
                ).render(),
                h.div(".text-end")[
                    h.input(
                        ".btn.btn-success.btn-lg",
                        type="submit",
                        value=tdt("Modify"),
                    ),
                ],
            ],
        ]


class ProjectPreviewModal(ModalBaseTemplate):
    def title(self):
        return tdt("Project preview")

    def body(self):
        obj = self.context["object"]
        return [
            h.h2[obj.name],
            h.table(".table")[
                h.tbody[
                    h.tr[
                        h.th[tdt("description")],
                        h.td[obj.description],
                    ],
                    h.tr[
                        h.td[tdt("business ID")],
                        h.td[obj.business_key],
                    ],
                ],
            ],
            h.a(
                href=reverse("edit_project", args=[obj.id]),
                class_="btn btn-primary",
            )[tdt("Edit project")],
        ]
