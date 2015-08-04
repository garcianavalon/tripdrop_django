from __future__ import absolute_import, unicode_literals

import json
from itertools import chain
import logging
import re

from django import forms
from django.core.urlresolvers import reverse
from django.core.validators import EMPTY_VALUES
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.utils.six import text_type


logger = logging.getLogger(__name__)

class Select2Mixin(object):
    """Base methods for Select2 style widgets"""

    options = {
        'minimumResultsForSearch': 6,  # Only applicable for single value select.
        'placeholder': '',  # Empty text label
        'allowClear': True,  # Not allowed when field is multiple since there each value has a clear button.
        'multiple': False,  # Not allowed when attached to <select>
        'closeOnSelect': False,
    }

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
                or are not applicable in some scenarios. For example, when Select2 is attached to a ``<select>`` tag,
                it can detect if it is being used with a single or multiple values from that tag itself. If you specified the
                ``multiple`` option in this case, it would not only be useless but an error from Select2 JS' point of view.
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

    def get_options(self):
        """
        :return: Dictionary of options to be passed to Select2 JS.
        :rtype: :py:obj:`dict`
        """
        options = dict(self.options)
        if options.get('allowClear', None) is not None:
            options['allowClear'] = not self.is_required
        if options.get('placeholder'):
            options['placeholder'] = force_text(options['placeholder'])
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


# AJAX
class AjaxSelect2Mixin(Select2Mixin):
    """
    The base mixin of all Heavy Select2 widgets. It sub-classes :py:class:`Select2Mixin`.
    This mixin adds more Select2 options to :py:attr:`.Select2Mixin.options`. These are:-
        * minimumInputLength: ``2``
        * initSelection: ``'django_select2.onInit'``
        * ajax:
            * dataType: ``'json'``
            * quietMillis: ``100``
            * data: ``'django_select2.get_url_params'``
            * results: ``'django_select2.process_results'``
    .. tip:: You can override these options by passing ``select2_options`` kwarg to :py:meth:`.__init__`.
    """

    def __init__(self, **kwargs):
        """
        Constructor of the class.
        The following kwargs are allowed:-
        :param data_view: A :py:class:`~.views.Select2View` sub-class which can respond to this widget's Ajax queries.
        :type data_view: :py:class:`django.views.generic.base.View` or None
        :param data_url: Url which will respond to Ajax queries with JSON object.
        :type data_url: :py:obj:`str` or None
        .. tip:: When ``data_view`` is provided then it is converted into an URL using
            :py:func:`~django.core.urlresolvers.reverse`.
        .. warning:: Either of ``data_view`` or ``data_url`` must be specified, otherwise :py:exc:`ValueError` will
            be raised.
        :param choices: The list of available choices. If not provided then empty list is used instead. It
            should be of the form -- ``[(val1, 'Label1'), (val2, 'Label2'), ...]``.
        :type choices: :py:obj:`list` or :py:obj:`tuple`
        :param userGetValTextFuncName: The name of the custom JS function which you want to use to convert
            value to label.
            In ``heavy_data.js``, ``django_select2.getValText()`` employs the following logic to convert value
            to label :-
                1. First check if the Select2 input field has ``txt`` attribute set along with ``value``. If found
                then use it.
                2. Otherwise, check if user has provided any custom method for this. Then use that. If it returns a
                label then use it.
                3. Otherwise, check the cached results. When the user searches in the fields then all the returned
                responses from server, which has the value and label mapping, are cached by ``heavy_data.js``.
        :type userGetValTextFuncName: :py:obj:`str`
        .. tip:: Since version 3.2.0, cookies or localStorage are no longer checked or used. All
            :py:class:`~.field.HeavyChoiceField` must override :py:meth:`~.fields.HeavyChoiceField.get_val_txt`.
            If you are only using heavy widgets in your own fields then you should override :py:meth:`.render_texts`.
        """
        self.field = None
        self.options = dict(self.options)  # Making an instance specific copy
        self.view = kwargs.pop('data_view', None)
        self.url = kwargs.pop('data_url', None)
        self.userGetValTextFuncName = kwargs.pop('userGetValTextFuncName', 'null')
        self.choices = kwargs.pop('choices', [])

        if not self.view and not self.url:
            raise ValueError('data_view or data_url is required')

        self.options['ajax'] = {
            'dataType': 'json',
            'delay': 250,
            'cache': True,
            'data': 'function(params){var queryParameters = {q:params.term}return queryParameters;}',
            'processResults': 'function(data){return {results:data};}',
        }
        self.options['minimumInputLength'] = 2
        # self.options['initSelection'] = 'django_select2.onInit'
        super(AjaxSelect2Mixin, self).__init__(**kwargs)

    def get_options(self):

        if self.url is None:
            # We lazy resolve the view. By this time Url conf would been loaded fully.
            self.url = reverse(self.view)

        if self.options['ajax'].get('url', None) is None:
            self.options['ajax']['url'] = self.url

        return super(AjaxSelect2Mixin, self).get_options()


    def render_inner_js_code(self, id_, name, value, attrs=None, choices=(), *args):
        #js = '$(hashedSelector).change(django_select2.onValChange).data("userGetValText", null);'
        js = ''
        # texts = self.render_texts_for_value(id_, value, choices)
        # if texts:
        #     js += texts
        js += super(AjaxSelect2Mixin, self).render_inner_js_code(id_, name, value, attrs, choices, *args)
        return js


class AjaxSelect2Widget(AjaxSelect2Mixin, forms.Select):
    """
    Single selection heavy widget.
    Following Select2 option from :py:attr:`.Select2Mixin.options` is added or set:-
        * multiple: ``False``
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
        return super(AjaxSelect2Widget, self).render_options(choices, selected_choices)

    # def render_inner_js_code(self, id_, *args):
    #     field_id = self.field_id if hasattr(self, 'field_id') else id_
    #     fieldset_id = re.sub(r'-\d+-', '_', id_).replace('-', '_')
    #     if '__prefix__' in id_:
    #         return ''
    #     else:
    #         js = '''
    #               window.django_select2.%s = function (selector, fieldID) {
    #                 var hashedSelector = "#" + selector;
    #                 $(hashedSelector).data("field_id", fieldID);
    #               ''' % (fieldset_id)
    #         js += super(AjaxSelect2Widget, self).render_inner_js_code(id_, *args)
    #         js += '};'
    #         js += 'django_select2.%s("%s", "%s");' % (fieldset_id, id_, field_id)
    #         return js