
from django import forms

from django_select2 import fields as select2_fields
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, ButtonHolder, Submit

import needs.models as need_models

class CityChoices(select2_fields.ModelSelect2Field):
    queryset = need_models.City.objects
    search_fields = ['name__icontains', ]

# ModelForms
class NeedForm(forms.ModelForm):
    city = CityChoices()

    def __init__(self, *args, **kwargs):
        super(NeedForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)


    class Meta:
        model = need_models.Need
        # TODO(garcianavalon) this is ok for prototyping but should set explicit
        # fields for production to avoid security vulnerabilities
        fields = ['petition']