import json
import logging

from django import forms
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe


logger = logging.getLogger(__name__)

class GoogleMapsMixin(object):
    """docstring for GoogleMapsMixin"""

    default_options = {
        'zoom': 8,
        'center': {
            'lat': -34.397,
            'lng': 150.644
        }
    }

    def __init__(self, *args, **kwargs):
        self.options = self.default_options.copy()
        self.options.update(kwargs.pop('options'))

        super(GoogleMapsMixin, self).__init__(*args, **kwargs)

    def get_options(self):
        return json.dumps(self.options)

    def render(self, name, value, attrs):
        output = super(GoogleMapsMixin, self).render(name, value, attrs)

        output += u'<div id="map_{id}" class="map map-container" style="height:500px"></div>'.format(id=attrs['id'])

        output += u'<script type="text/javascript">var options_map_{id} = {json};</script>'.format(
            id=attrs['id'], json=self.get_options())

        return mark_safe(output)

    class Media:
        js = ('maps/js/widget.js',)


class GoogleMapGeoLocationWidget(GoogleMapsMixin, forms.TextInput):
    pass
    