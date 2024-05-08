import qrcode
from io import BytesIO
from base64 import b64encode

from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse

from wireguard import forms, models
from wireguard.core import tools
from wireguard.core import keygen
from core.tools import get_values_list
from core.views import RestrictedMixin


class CreateInterfaceView(RestrictedMixin, generic.CreateView):
    
    template_name = 'components/form.html'
    form_class = forms.InterfaceForm
    model = models.Interface
    success_url = reverse_lazy('dashboard:networks')
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'form_button': 'Create Network',
            'form_action': reverse('wireguard:create-interface'),
            'form_hx': True
        })
        return context
    
    def get_form(self, form_class: BaseModelForm = None) -> BaseModelForm:
        form = super().get_form(form_class)
        form.fields['name'].widget.attrs['autofocus'] = True
        return form
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.listen_port = self._get_port()
        form.instance.subnet_num = self._get_subnet()
        keys = keygen.generate_keys()
        form.instance.private_key = keys['private']
        form.instance.public_key = keys['public']
        return super().form_valid(form)
    
    def _get_port(self):
        occupied_ports = get_values_list(self.model.objects.all(), 'listen_port')
        return tools.get_vacant_port(occupied_ports)
    
    def _get_subnet(self):
        occupied_subnets = get_values_list(self.model.objects.all(), 'subnet_num')
        return tools.get_vacant_address(occupied_subnets)
    
    def post(self, request: HttpRequest, *args: str, **kwargs) -> HttpResponse:
        response = super().post(request, *args, **kwargs)
        return response
    
    
class UpdateInterfaceView(RestrictedMixin, generic.UpdateView):
    
    template_name = 'components/update-form.html'
    model = models.Interface
    form_class = forms.InterfaceForm
    success_url = reverse_lazy('dashboard:networks')
    
    def get_context_data(self, **kwargs):
        kwargs.update({
            'form_action': reverse('wireguard:update-interface', args=[self.kwargs['pk']]),
            'delete_action': reverse('wireguard:delete-interface', args=[self.kwargs['pk']])
        })
        return super().get_context_data(**kwargs)
    

class DeleteInterfaceView(RestrictedMixin, generic.DeleteView):
    
    model = models.Interface
    success_url = reverse_lazy('dashboard:networks')
    template_name = 'components/form.html'
    
    def get_context_data(self, **kwargs):
        kwargs.update({
            'form_action': reverse('wireguard:delete-interface', args=[self.kwargs['pk']]),
            'form_button': 'Confirm Delete...',
            'form_button_type': 'danger'
        })
        return super().get_context_data(**kwargs)

    
class CreatePeerView(RestrictedMixin, generic.CreateView):
    
    form_class = forms.PeerForm
    template_name = 'components/form.html'
    model = models.Peer
    success_url = reverse_lazy('dashboard:peers')
    
    def get_context_data(self, **kwargs):
        kwargs.update({
            'form_button': 'Create Peer',
            'form_action': reverse('wireguard:create-peer'),
            'form_hx': True
        })
        return super().get_context_data(**kwargs)
    
    def get_form(self, form_class: BaseModelForm = None) -> BaseModelForm:
        form = super().get_form(form_class)
        form.fields['name'].widget.attrs['autofocus'] = True
        return form

    def form_valid(self, form: BaseModelForm):
        keys = keygen.generate_keys()
        form.instance.private_key = keys['private']
        form.instance.public_key = keys['public']
        form.instance.preshared_key = keys['preshared']
        form.instance.ip_num = self._get_ip(form.instance.interface)
        return super().form_valid(form)
    
    def _get_ip(self, interface):
        peer_ips = [1]
        peer_ips.extend(get_values_list(interface.peers.all(), 'ip_num'))
        return tools.get_vacant_address(peer_ips)
    

class UpdatePeerView(RestrictedMixin, generic.UpdateView):
    
    template_name = 'components/update-form.html'
    model = models.Peer
    form_class = forms.PeerForm
    success_url = reverse_lazy('dashboard:peers')
    
    def get_context_data(self, **kwargs):
        kwargs.update({
            'form_action': reverse('wireguard:update-peer', args=[self.kwargs['pk']]),
            'delete_action': reverse('wireguard:delete-peer', args=[self.kwargs['pk']])
        })
        return super().get_context_data(**kwargs)
    
    def get_form(self) -> BaseModelForm:
        form = super().get_form()
        form.fields['interface'].widget.attrs['disabled'] = True
        return form
    
    def get_form_kwargs(self) -> dict:
        kwargs = super().get_form_kwargs()
        if self.request.method == 'POST':
            data = {k:v for k,v in self.request.POST.items()}
            data['interface'] = self.get_object().interface.id
            kwargs['data'] = data
        return kwargs
        
    
class DeletePeerView(RestrictedMixin, generic.DeleteView):
    
    model = models.Peer
    success_url = reverse_lazy('dashboard:peers')
    template_name = 'components/form.html'
    
    def get_context_data(self, **kwargs):
        kwargs.update({
            'form_action': reverse('wireguard:delete-peer', args=[self.kwargs['pk']]),
            'form_button': 'Confirm Delete...',
            'form_button_type': 'danger'
        })
        return super().get_context_data(**kwargs)
    
    
class DownloadPeerConfigView(RestrictedMixin, generic.View):
    
    def get(self, *args, **kwargs):
        peer = models.Peer.objects.get(pk=kwargs['pk'])
        filename = f'{peer.interface.name}-{peer.name}.conf'
        response = HttpResponse(peer.flush(), content_type="application/text")
        response['Content-Disposition'] = f'inline; filename={filename}'
        return response
    
    
class QrPeerConfigView(RestrictedMixin, generic.View):
    
    def get(self, *args, **kwargs):
        peer = models.Peer.objects.get(pk=kwargs['pk'])
        img = qrcode.make(peer.flush(), box_size=6)
        stream = BytesIO()
        img.save(stream, 'png')
        image_data = b64encode(stream.getvalue()).decode('utf-8')
        response = f'<img src="data:image/png;base64,{image_data}">'
        return HttpResponse(response)
    
    
class ShowPeerConfigView(RestrictedMixin, generic.View):
    
    def get(self, *args, **kwargs):
        peer = models.Peer.objects.get(pk=kwargs['pk'])
        response = HttpResponse(peer.flush(), content_type="application/text")
        # response['Content-Disposition'] = f'inline; filename={filename}'
        return response
        