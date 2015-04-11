from django.views.generic import ListView
import needs.models as needs_models

class NeedList(ListView):
    model = needs_models.Need
    template_name = 'needs/need_list.html'