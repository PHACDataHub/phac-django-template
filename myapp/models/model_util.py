from django.utils.translation import get_language

from proj import fields


class BilingualNameMixin:
    name_en = fields.CharField(max_length=255, unique=True)
    name_fr = fields.CharField(max_length=255, unique=True)

    @property
    def name(self):
        return getattr(self, f"name_{get_language()}")


class BilingualDescriptionMixin:
    description_en = fields.TextField(blank=True, null_to_empty=True)
    description_fr = fields.TextField(blank=True, null_to_empty=True)

    @property
    def description(self):
        return getattr(self, f"description_{get_language()}")
