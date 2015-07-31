from __future__ import absolute_import, unicode_literals

import json
import logging
from itertools import chain

from django import forms
from django.utils.safestring import mark_safe
from django.utils.six import text_type


logger = logging.getLogger(__name__)

class Select2Mixin(object):

    def __init__(self, **kwargs):
        """
        Constructor of the class.
        The following additional kwarg is allowed:-
        :param select2_options: This is similar to standard Django way to pass extra attributes to widgets.
            This is meant to override values of existing :py:attr:`.options`.
            Example::
                class MyForm(ModelForm):
                    class Meta:
                        model = MyModel
                        widgets = {
                            'name': Select2WidgetName(select2_options={
                                'minimumResultsForSearch': 10,
                                'closeOnSelect': True,
                                })
                        }
        :type select2_options: :py:obj:`dict` or None
        """
        super(Select2Mixin, self).__init__(**kwargs)

        self.options = kwargs.pop('select2_options', None)
        self.options['allowClear'] = not self.is_required

    def render_js_code(self, id_, *args):
        """
        Renders the ``<script>`` block which contains the JS code for this widget.
        :return: The rendered JS code enclosed inside ``<script>`` block.
        :rtype: :py:obj:`unicode`
        """
        return self.render_js_script(self.render_inner_js_code(id_, *args))

    def render_js_script(self, inner_code):
        """
        This wraps ``inner_code`` string inside the following code block::
            <script type="text/javascript">
                $(function () {
                    // inner_code here
                });
            </script>
        :rtype: :py:obj:`unicode`
        """
        return """
                <script type="text/javascript">
                    $(function () {
                        %s
                    });
                </script>
                """ % inner_code

    def render_inner_js_code(self, id_, *args):
        """
        Renders all the JS code required for this widget.
        :return: The rendered JS code which will be later enclosed inside ``<script>`` block.
        :rtype: :py:obj:`unicode`
        """
        options = json.dumps(self.get_options())
        #options = options.replace('"*START*', '').replace('*END*"', '')
        return '$(#{id}).select2({options});'.format(
        	id=id_, options=options)

    def render(self, name, value, attrs=None, choices=()):
        """
        Renders this widget. HTML and JS code blocks all are rendered by this.
        :return: The rendered markup.
        :rtype: :py:obj:`unicode`
        """

        args = [name, value, attrs]
        if choices:
            args.append(choices)

        s = text_type(super(Select2Mixin, self).render(*args))  # Thanks to @ouhouhsami Issue#1
        s += self.media.render()
        final_attrs = self.build_attrs(attrs)
        id_ = final_attrs.get('id', None)
        s += self.render_js_code(id_, name, value, attrs, choices)

        return mark_safe(s)

    class Media:
        pass


        