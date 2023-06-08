from django.db import models

from proj import fields
from proj.model_util import add_to_admin, track_versions
from proj.models import User
from proj.text import tdt


class ProjectUserRole(models.Model):
    SPECTATOR_ROLE = "spectator"
    CONTRIBUTOR_ROLE = "contributor"
    LEADER_ROLE = "leader"

    ROLE_CHOICES = (
        (SPECTATOR_ROLE, tdt("Spectator")),
        (CONTRIBUTOR_ROLE, tdt("Contributor")),
        (LEADER_ROLE, tdt("Leader")),
    )

    project = fields.ForeignKey(
        "my_app.Project", related_name="roles", on_delete=models.CASCADE
    )
    user = fields.ForeignKey(
        User, related_name="project_roles", on_delete=models.CASCADE
    )
    role = fields.CharField(max_length=50, choices=ROLE_CHOICES)
