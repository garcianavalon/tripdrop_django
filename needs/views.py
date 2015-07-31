from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import needs.models as needs_models
import needs.forms as needs_forms

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
    success_url = reverse_lazy('needs:index')



