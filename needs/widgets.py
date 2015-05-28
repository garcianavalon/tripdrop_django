from __future__ import absolute_import, unicode_literals

import json
import logging
from itertools import chain

from django import forms
from django.utils.safestring import mark_safe
from django.utils.six import text_type


logger = logging.getLogger(__name__)

class Select2Mixin(object):
    """
    The base mixin of all Select2 widgets.
    This mixin is responsible for rendering the necessary JavaScript and CSS codes which turns normal ``<select>``
    markups into Select2 choice list.
    The following Select2 options are added by this mixin:-
        * minimumResultsForSearch: ``6``
        * placeholder: ``''``
        * allowClear: ``True``
        * multiple: ``False``
        * closeOnSelect: ``False``
    .. note:: Many of them would be removed by sub-classes depending on requirements.
    """

    # For details on these options refer: http://ivaynberg.github.com/select2/#documentation
    options = {
        'minimumResultsForSearch': 6,  # Only applicable for single value select.
        'placeholder': '',  # Empty text label
        'allowClear': True,  # Not allowed when field is multiple since there each value has a clear button.
        'multiple': False,  # Not allowed when attached to <select>
        'closeOnSelect': False,
    }
    """
    The options listed here are rendered as JS map and passed to Select2 JS code.
    Complete description of these options are available in Select2_ JS' site.
    .. _Select2: http://ivaynberg.github.com/select2/#documentation.
    """

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
            .. tip:: You cannot introduce new options using this. For that you should sub-class and override
                :py:meth:`.init_options`. The reason for this is, few options are not compatible with each other
                or are not applicable in some scenarios. For example, when Select2 is attached to ``<select>`` tag,
                it can get if it is multiple or single valued from that tag itself. In this case if you specify
                ``multiple`` option then not only it is useless but an error in Select2 JS' point of view.
                There are other such intricacies, based on which some options are removed. By enforcing this
                restriction we make sure to not break the code by passing some wrong concoction of options.
            .. tip:: According to the select2 documentation, in order to get the ``placeholder`` and ``allowClear``
                settings working, you have to specify an empty ``<option></option>`` as the first entry in your
                ``<select>`` list. Otherwise the field will be rendered without a placeholder and the clear feature
                will stay disabled.
        :type select2_options: :py:obj:`dict` or None
        """
        # Making an instance specific copy
        self.options = dict(self.options)
        select2_options = kwargs.pop('select2_options', None)
        if select2_options:
            for name, value in select2_options.items():
                self.options[name] = value
        self.init_options()

        super(Select2Mixin, self).__init__(**kwargs)

    def init_options(self):
        """
        Sub-classes can use this to suppress or override options passed to Select2 JS library.
        Example::
            def init_options(self):
                self.options['createSearchChoice'] = 'Your_js_function'
        In the above example we are setting ``Your_js_function`` as Select2's ``createSearchChoice``
        function.
        """
        pass

    def set_placeholder(self, val):
        """
        Placeholder is a value which Select2 JS library shows when nothing is selected. This should be string.
        :return: None
        """
        self.options['placeholder'] = val

    def get_options(self):
        """
        :return: Dictionary of options to be passed to Select2 JS.
        :rtype: :py:obj:`dict`
        """
        options = dict(self.options)
        if options.get('allowClear', None) is not None:
            options['allowClear'] = not self.is_required
        return options

    def render_js_code(self, id_, *args):
        """
        Renders the ``<script>`` block which contains the JS code for this widget.
        :return: The rendered JS code enclosed inside ``<script>`` block.
        :rtype: :py:obj:`unicode`
        """
        if id_:
            return self.render_js_script(self.render_inner_js_code(id_, *args))
        return ''

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
        options = options.replace('"*START*', '').replace('*END*"', '')
        js = 'var hashedSelector = "#" + "%s";' % id_
        js += '$(hashedSelector).select2(%s);' % (options)
        return js

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


class Select2Widget(Select2Mixin, forms.Select):
    """
    Drop-in Select2 replacement for :py:class:`forms.Select`.
    Following Select2 option from :py:attr:`.Select2Mixin.options` is removed:-
        * multiple
    """

    def init_options(self):
        self.options.pop('multiple', None)

    def render_options(self, choices, selected_choices):
        all_choices = chain(self.choices, choices)
        if not self.is_required \
                and len([value for value, txt in all_choices if value == '']) == 0:
            # Checking if list already has empty choice
            # as in the case of Model based Light fields.
            choices = list(choices)
            choices.append(('', '', ))  # Adding an empty choice
        return super(Select2Widget, self).render_options(choices, selected_choices)


class Select2MultipleWidget(Select2Mixin, forms.SelectMultiple):
    """
    Drop-in Select2 replacement for :py:class:`forms.SelectMultiple`.
    Following Select2 options from :py:attr:`.Select2Mixin.options` are removed:-
        * multiple
        * allowClear
        * minimumResultsForSearch
    """

    def init_options(self):
        self.options.pop('multiple', None)
        self.options.pop('allowClear', None)
        self.options.pop('minimumResultsForSearch', None)

        