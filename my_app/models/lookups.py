from django.db import models

from proj import fields
from proj.model_util import add_to_admin, track_versions

from .model_util import BilingualDescriptionMixin, BilingualNameMixin


@track_versions
@add_to_admin
class ProjectType(models.Model, BilingualDescriptionMixin, BilingualNameMixin):
    code = fields.CharField(
        max_length=100, unique=True
    )  # codes are dev-friendly identifiers so we can hard-code behaviour for particular project types


@track_versions
@add_to_admin
class ProjectTag(models.Model, BilingualNameMixin, BilingualDescriptionMixin):
    pass
