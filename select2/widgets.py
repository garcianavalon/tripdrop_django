import copy
import json
import logging

from django import forms
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe



LOG = logging.getLogger(__name__)

class Select2Mixin(object):
    """docstring for Select2Mixin"""

    default_select2_options = {
        'minimumInputLength': 0,
    }

    def __init__(self, *args, **kwargs):
        self.select2_options = copy.deepcopy(self.default_select2_options)
        self.select2_options.update(kwargs.pop('select2_options'))

        super(Select2Mixin, self).__init__(*args, **kwargs)

    def get_select2_options(self):
        return json.dumps(self.select2_options)

    def render(self, name, value, attrs):
        output = super(Select2Mixin, self).render(name, value, attrs)

        output += u'<script type="text/javascript">var select2_{id} = {json};</script>'.format(
            id=attrs['id'], json=self.get_select2_options())

        return mark_safe(output)

    class Media:
        js = ('select2/js/test.js',)


class Select2Widget(Select2Mixin, forms.Select):
    pass
    

class Select2MultipleWidget(Select2Mixin, forms.SelectMultiple):
    pass


class Select2AjaxWidget(Select2Widget):

    default_ajax_options = {
        'delay': 250,
    }

    default_select2_options = {
        'minimumInputLength': 2,
    }

    def __init__(self, *args, **kwargs):
        ajax_options = kwargs.pop('ajax_options')
        
        super(Select2AjaxWidget, self).__init__(*args, **kwargs)
        
        self.select2_options['ajax'] = copy.deepcopy(self.default_ajax_options)
        self.select2_options['ajax'].update(ajax_options)


    def get_select2_options(self):
        select2_options = copy.deepcopy(self.select2_options)
        if 'url' in select2_options['ajax']:
            select2_options['ajax']['url'] = reverse(select2_options['ajax']['url'])
        return json.dumps(select2_options)