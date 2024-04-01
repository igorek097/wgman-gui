from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

from core.forms import BootstrapFormMixin


class SignupForm(BootstrapFormMixin, UserCreationForm):
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2']
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.help_text = None
            
            
class LoginForm(BootstrapFormMixin, AuthenticationForm):
    pass
        