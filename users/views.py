from django.core.urlresolvers import reverse_lazy
from django.views import generic

# Create your views here.
class ProfileView(generic.TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)

        if self.request.user.is_authenticated():
            context['user'] = self.request.user

        return context
