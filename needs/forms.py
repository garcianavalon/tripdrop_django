from django import forms

from django_select2 import fields as select2_fields
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, ButtonHolder, Submit
from django_countries import countries

import needs.models as need_models

# ModelForms
class NeedForm(forms.ModelForm):
    city = select2_fields.ModelSelect2Field(queryset=need_models.City.objects)
    #region = select2_fields.ModelSelect2Field(queryset=need_models.Region.objects)
    #country = select2_fields.Select2ChoiceField(choices=countries)

    def __init__(self, *args, **kwargs):
        super(NeedForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)


    class Meta:
        model = need_models.Need
        # TODO(garcianavalon) this is ok for prototyping but should set explicit
        # fields for production to avoid security vulnerabilities
        fields = []