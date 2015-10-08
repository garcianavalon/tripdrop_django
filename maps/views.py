from django.core.urlresolvers import reverse_lazy
from django.views import generic

class BaseMapView(generic.TemplateView):
    template_name = 'maps/base_map.html'
