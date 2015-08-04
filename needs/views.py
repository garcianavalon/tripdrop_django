from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import needs.models as needs_models
import needs.forms as needs_forms
from select2 import views as select2_views

class NeedList(ListView):
    model = needs_models.Need
    template_name = 'needs/need_list.html'

class NeedCreate(CreateView):
    model = needs_models.Need
    form_class = needs_forms.NeedForm

class NeedDetail(DetailView):
    model = needs_models.Need

class NeedUpdate(UpdateView):
    model = needs_models.Need
    # TODO(garcianavalon) this is ok for prototyping but should set explicit
    # fields for production to avoid security vulnerabilities
    fields = '__all__'

class NeedDelete(DeleteView):
    model = needs_models.Need
    success_url = reverse_lazy('needs:list')


class MunicipalityList(select2_views.Select2View):

    def get_results(self, request, term, page, context):
        """
        Returns the result for the given search ``term``.
        :param request: The Ajax request object.
        :type request: :py:class:`django.http.HttpRequest`
        :param term: The search term.
        :type term: :py:obj:`str`
        :param page: The page number. If in your last response you had signalled that there are more results,
            then when user scrolls more a new Ajax request would be sent for the same term but with next page
            number. (Page number starts at 1)
        :type page: :py:obj:`int`
        :param context: Can be anything which persists across the lifecycle of queries for the same search term.
            It is reset to ``None`` when the term changes.
            .. note:: Currently this is not used by ``heavy_data.js``.
        :type context: :py:obj:`str` or None
        Expected output is of the form::
            (err, has_more, [results])
        Where ``results = [(id1, text1), (id2, text2), ...]``
        For example::
            ('nil', False,
                [
                (1, 'Value label1'),
                (20, 'Value label2'),
                ])
        When everything is fine then the `err` must be 'nil'.
        `has_more` should be true if there are more rows.
        """
        return ('nil', False,
                [
                (1, 'Value label1'),
                (20, 'Value label2'),
                ])

