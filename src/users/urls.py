from django.urls import path
from django.contrib.auth.views import LogoutView

from users import views


app_name = 'users'


urlpatterns = [
    path('signup', views.SignupView.as_view(), name='signup'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
]