from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.contrib.auth import views as auth_views, get_user_model
from django.contrib.auth import logout

from users import forms


class SignupView(CreateView):
    
    success_url = reverse_lazy('dashboard:networks')
    form_class = forms.SignupForm
    model = get_user_model()
    template_name = 'users/signup.html'
    
    def get(self, request, *args, **kwargs) -> HttpResponse:
        if get_user_model().objects.count():
            return HttpResponseRedirect(reverse('core:main'))
        return super().get(request, *args, **kwargs)

    
#TODO: figure out redirect logic and optimize
class LoginView(auth_views.LoginView):
    
    success_url = reverse_lazy('dashboard:networks')
    model = get_user_model()
    form_class = forms.LoginForm
    fields = ['username', 'password']
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    
    def get(self, request, *args, **kwargs) -> HttpResponse:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('core:main'))
        return super().get(request, *args, **kwargs)
    
    def get_success_url(self) -> str:
        return self.success_url
    
    
class LogoutView(auth_views.LogoutView):
    
    http_method_names = ['get']
    template_name = 'users/logout.html'
    
    def get(self, request, *args, **kwargs) -> HttpResponse:
        logout(request)
        return super().get(request, *args, **kwargs)