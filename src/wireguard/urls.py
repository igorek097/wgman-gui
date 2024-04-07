from django.urls import path
from wireguard import views


app_name = 'wireguard'


urlpatterns = [
    path('create-interface', views.CreateInterfaceView.as_view(), name='create-interface'),
    path('update-interface/<pk>', views.UpdateInterfaceView.as_view(), name='update-interface'),
    path('delete-interface/<pk>', views.DeleteInterfaceView.as_view(), name='delete-interface'),
    
    path('create-peer', views.CreatePeerView.as_view(), name='create-peer'),
    path('update-peer/<pk>', views.UpdatePeerView.as_view(), name='update-peer'),
    path('delete-peer/<pk>', views.DeletePeerView.as_view(), name='delete-peer'),
    path('download-peer-config/<pk>', views.DownloadPeerConfigView.as_view(), name='download-peer-config'),
    path(f'qr-peer-config/<pk>', views.QrPeerConfigView.as_view(), name='qr-peer-config'),
]