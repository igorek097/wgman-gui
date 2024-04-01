from django.views import generic
from django.db.models import Q

from core.views import RestrictedMixin
from wireguard.models import Interface, Peer



class NetworksView(RestrictedMixin, generic.ListView):
    
    template_name = 'dashboard/networks.html'
    model = Interface
    
    def get_context_data(self, **kwargs):
        kwargs['section'] = 1
        return super().get_context_data(**kwargs)
    
    
class PeersView(RestrictedMixin, generic.ListView):
    
    template_name = 'dashboard/peers.html'
    model = Peer
    
    def get_context_data(self, **kwargs):
        kwargs['section'] = 2
        if 'search' in self.request.GET:
            kwargs['search'] = self.request.GET['search']
        return super().get_context_data(**kwargs)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if 'search' in self.request.GET:
            q = self.request.GET['search']
            queryset = queryset.filter(Q(name__icontains=q) | Q(interface__name__icontains=q))
        return queryset
    