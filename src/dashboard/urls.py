from django.urls import path
from dashboard import views


app_name = 'dashboard'


urlpatterns = [
    path('networks', views.NetworksView.as_view(), name='networks'),
    path('peers', views.PeersView.as_view(), name='peers'),
]