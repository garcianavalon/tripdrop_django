from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, ButtonHolder, Submit
from django_countries import countries

import needs.models as need_models
import needs.widgets as need_widgets

# ModelForms
class NeedForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(NeedForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)


    class Meta:
        model = need_models.Need
        # TODO(garcianavalon) this is ok for prototyping but should set explicit
        # fields for production to avoid security vulnerabilities
        fields = '__all__'