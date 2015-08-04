from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, ButtonHolder, Submit
from django_countries import countries

import needs.models as need_models
import select2.widgets as select2_widgets

# ModelForms
class NeedForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(NeedForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Submit'))


    class Meta:
        model = need_models.Need
        # TODO(garcianavalon) this is ok for prototyping but should set explicit
        # fields for production to avoid security vulnerabilities
        fields = '__all__'

        widgets = {
            'need_type': select2_widgets.Select2Widget(),
            'municipality': select2_widgets.AjaxSelect2Widget(
                data_view='needs:list_municipalities'),
        }