from django.db import models

from proj import fields
from proj.model_util import add_to_admin, track_versions
from proj.text import tdt

from .model_util import BilingualDescriptionMixin, BilingualNameMixin


@track_versions
@add_to_admin
class Project(models.Model, BilingualDescriptionMixin, BilingualNameMixin):
    ACTIVE_STATUS = "active"
    ONHOLD_STATUS = "onhold"
    CANCELLED_STATUS = "cancelled"
    COMPLETED_STATUS = "completed"
    STATUS_CHOICES = (
        (ACTIVE_STATUS, tdt("Active")),
        (ONHOLD_STATUS, tdt("On Hold")),
        (CANCELLED_STATUS, tdt("Cancelled")),
        (COMPLETED_STATUS, tdt("Completed")),
    )

    business_key = fields.CharField(max_length=50, unique=True)
    status = fields.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        null=False,
        default=ACTIVE_STATUS,
    )


@track_versions
@add_to_admin
class ProjectTask(models.Model, BilingualDescriptionMixin, BilingualNameMixin):
    project = fields.ForeignKey(
        "Project", related_name="tasks", on_delete=models.CASCADE
    )
