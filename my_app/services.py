from my_app.models import ProjectUserRole


def _set_project_user_role(proj, user, role):
    current_role = proj.get_user_role(user)
    if current_role:
        current_role.role = role
        current_role.save()
    else:
        ProjectUserRole.objects.create(project=proj, user=user, role=role)


def set_project_leader(proj, user):
    _set_project_user_role(proj, user, ProjectUserRole.LEADER_ROLE)


def set_project_contributor(proj, user):
    _set_project_user_role(proj, user, ProjectUserRole.CONTRIBUTOR_ROLE)


def set_project_spectator(proj, user):
    _set_project_user_role(proj, user, ProjectUserRole.SPECTATOR_ROLE)
