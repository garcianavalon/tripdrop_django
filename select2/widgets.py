import json
import logging

from django import forms
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe



logger = logging.getLogger(__name__)


class Select2Widget(forms.Select):

    def __init__(self, *args, **kwargs):
        self.select2_options = kwargs.pop('select2_options')
        super(Select2Widget, self).__init__(*args, **kwargs)

    def get_select2_options(self):
        return json.dumps(self.select2_options)

    def render(self, name, value, attrs):
        output = super(Select2Widget, self).render(name, value, attrs)

        output += u'<script type="text/javascript">var select2_{id} = {json};</script>'.format(
            id=attrs['id'], json=self.get_select2_options())

        return mark_safe(output)

    class Media:
        js = ('select2/js/test.js',)


class Select2AjaxWidget(Select2Widget):

    default_ajax_options = {
        'delay': 250,
    }

    def __init__(self, *args, **kwargs):
        ajax_options = kwargs.pop('ajax_options')
        
        super(Select2AjaxWidget, self).__init__(*args, **kwargs)
        
        self.select2_options['ajax'] = self.default_ajax_options
        self.select2_options['ajax'].update(ajax_options)

    def get_select2_options(self):
        if 'url' in self.select2_options['ajax']:
            self.select2_options['ajax']['url'] = reverse(self.select2_options['ajax']['url'])
        return json.dumps(self.select2_options)