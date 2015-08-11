from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from needs import models as needs_models
from needs import forms as needs_forms


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
    form_class = needs_forms.NeedForm

class NeedDelete(DeleteView):
    model = needs_models.Need
    success_url = reverse_lazy('needs:list')

    def get_context_data(self, **kwargs):
        context = super(NeedDelete, self).get_context_data(**kwargs)

        context['form'] = needs_forms.NeedDeleteForm()
        return context

def list_municipalities(request):
    """Select2 expects something like this
    data = {
        'results': [
            {
                'id': 'bar',
                'text': 'foo',
            },
            {
                'id': 'pepe',
                'text': 'pepe',
            },
        ]
    }
    """

    query_name = request.GET.get('q')
    if query_name:
        municipalities = needs_models.Municipality.objects.filter(name__istartswith=query_name)
        results = [{'id': m.id, 'text': m.name} for m in municipalities]
    else:
        results = []

    return JsonResponse({'results':results})

