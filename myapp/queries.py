from proj.rules_framework import test_rule

from myapp.models import Project, ProjectUserRole


def get_project_qs_for_user(user):
    if test_rule("is_admin", user):
        return Project.objects.all()

    roles = ProjectUserRole.objects.filter(user=user)
    proj_ids = [role.project_id for role in roles]
    return Project.objects.filter(id__in=proj_ids)
