from proj.rules_framework import add_rule, auto_rule

from .constants import ADMIN_USER_GROUP
from .models import ProjectUserRole


def get_roles(user, project_id):
    if not user.is_authenticated:
        return []
    return list(
        ProjectUserRole.objects.filter(user=user, project_id=project_id)
    )


@auto_rule
def is_admin(user):
    return user.is_authenticated and (
        user.is_superuser or ADMIN_USER_GROUP in user.group_names
    )


@auto_rule
def is_project_leader(user, project_id):
    roles = get_roles(user, project_id)
    return any(role.role == ProjectUserRole.LEADER_ROLE for role in roles)


@auto_rule
def is_project_contributor(user, project_id):
    roles = get_roles(user, project_id)
    return any(role.role == ProjectUserRole.CONTRIBUTOR_ROLE for role in roles)


@auto_rule
def is_project_spectator(user, project_id):
    roles = get_roles(user, project_id)
    return any(role.role == ProjectUserRole.SPECTATOR_ROLE for role in roles)


# Rules can be combined using boolean operators
add_rule("can_modify_project", is_admin | is_project_leader)
add_rule(
    "can_modify_project_tasks",
    is_admin | is_project_leader | is_project_contributor,
)
add_rule(
    "can_view_project",
    is_admin
    | is_project_leader
    | is_project_contributor
    | is_project_spectator,
)
