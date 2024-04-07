from django import forms
from core.forms import BootstrapFormMixin
from wireguard import models


class InterfaceForm(BootstrapFormMixin, forms.ModelForm):

    class Meta:
        model = models.Interface
        fields = ['name', 'dns', 'description', 'is_enabled']
        
        labels = {
            'name': 'Network name',
            'dns': 'DNS (optional)',
            'is_enabled': 'Enable Network?'
        }
        
        widgets = {
            'description': forms.Textarea(attrs={'rows':3}),
            'is_enabled': forms.CheckboxInput(),
        }
        
        
class PeerForm(BootstrapFormMixin, forms.ModelForm):
    
    class Meta:
        model = models.Peer
        fields = ['name', 'description', 'interface', 'is_enabled']
        
        labels = {
            'interface': 'Peer Network',
            'is_enabled': 'Enable Peer?'            
        }
        
        widgets = {
            'description': forms.Textarea(attrs={'rows':3}),
            'is_enabled': forms.CheckboxInput()
        }
        
        
class PeerUpdateForm(PeerForm):
    
    class Meta(PeerForm.Meta):
        
        widgets = {
            'description': forms.Textarea(attrs={'rows':3}),
            'is_enabled': forms.CheckboxInput(),
            'interface': forms.TextInput(attrs={'readonly':''})
        }
