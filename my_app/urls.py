from django.urls import path

from .views import project_crud as project_crud_views

urlpatterns = [
    path(
        "projects/",
        project_crud_views.ListProjects.as_view(),
        name="list_projects",
    ),
    path(
        "projects/create/",
        project_crud_views.CreateProject.as_view(),
        name="create_project",
    ),
    path(
        "projects/<int:pk>/preview_modal/",
        project_crud_views.ProjectPreviewModal.as_view(),
        name="preview_project_modal",
    ),
    path(
        "projects/<int:pk>/edit",
        project_crud_views.EditProject.as_view(),
        name="edit_project",
    ),
]
