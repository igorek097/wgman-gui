from django.views import generic
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy


class RestrictedMixin(LoginRequiredMixin):
    
    login_url = reverse_lazy('users:login')


#TODO: fill initial config

class MainView(generic.RedirectView):
    
    def get_redirect_url(self, *args, **kwargs):
        if not get_user_model().objects.count():
            return reverse('users:signup')
        if not self.request.user.is_authenticated:
            return reverse('users:login')
        return reverse('dashboard:networks')