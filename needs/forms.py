from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, ButtonHolder, Submit, HTML
from django_countries import countries

import needs.models as need_models
import select2.widgets as select2_widgets


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
            'need_type': select2_widgets.Select2Widget(
                select2_options={
                    'placeholder': 'Choose a type',
                }),
            'municipality': select2_widgets.Select2AjaxWidget(
                select2_options={
                    'placeholder': 'Choose a municipality',
                },
                ajax_options={
                    'url': 'needs:list_municipalities'
                }),
        }


class NeedDeleteForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(NeedDeleteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            HTML("<p>Are you sure you want to delete {{ object }}?</p>"),
            ButtonHolder(
                Submit('submit', 'Confirm')
            )
        )