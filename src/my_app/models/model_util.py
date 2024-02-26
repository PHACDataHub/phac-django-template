from django.db import models

from proj import fields
from proj.text import tdt
from proj.util import get_lang_code


class BilingualNameMixin(models.Model):
    class Meta:
        abstract = True

    name_en = fields.CharField(
        max_length=255, unique=True, verbose_name=tdt("Name (en)"), blank=False
    )
    name_fr = fields.CharField(
        max_length=255, unique=True, verbose_name=tdt("Name (fr)"), blank=False
    )

    @property
    def name(self):
        return getattr(self, f"name_{get_lang_code()}")


class BilingualDescriptionMixin(models.Model):
    class Meta:
        abstract = True

    description_en = fields.TextField(
        blank=True, null_to_empty=True, verbose_name=tdt("Description (en)")
    )
    description_fr = fields.TextField(
        blank=True, null_to_empty=True, verbose_name=tdt("Description (fr)")
    )

    @property
    def description(self):
        return getattr(self, f"description_{get_lang_code()}")
