from django import forms
from django.forms import widgets


class CustomDateInput(widgets.DateInput):
    input_type = "date"


class BootstrapMixin(forms.Form):
    template_name = "_generic_form.jinja2"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if isinstance(field.widget, widgets.Textarea):
                field.widget = widgets.Textarea(
                    attrs={
                        **field.widget.attrs,
                        "rows": 4,
                        "cols": 40,
                    }
                )
            if isinstance(field, (forms.FloatField, forms.DecimalField)):
                # right-align all numbers
                field.widget.attrs["class"] = (
                    field.widget.attrs.get("class", "") + " text-right "
                )

            if isinstance(field, forms.DateField):
                field.widget = CustomDateInput()
                field.widget.attrs["placeholder"] = "YYYY-MM-DD"

            if isinstance(field.widget, widgets.Select):
                # in addition to form-control, select widgets should have form-select
                field.widget.attrs["class"] = "form-select"

            if not isinstance(
                field.widget, (widgets.CheckboxInput, widgets.RadioSelect)
            ):
                # all other widgets get .form-control
                field.widget.attrs["class"] = (
                    field.widget.attrs.get("class", "") + " form-control"
                )
