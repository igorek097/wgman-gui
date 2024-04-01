from typing import Any
from django.db import models
from django.template.loader import render_to_string

from core.models import Setting
from core.tools import write_to_file


class Interface(models.Model):
    
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)
    subnet_num = models.SmallIntegerField()
    listen_port = models.PositiveIntegerField(unique=True)
    private_key = models.CharField(max_length=255)
    public_key = models.CharField(max_length=255)
    is_enabled = models.BooleanField(default=True)
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.was_enabled = self.is_enabled
    
    def __str__(self) -> str:
        return f'{self.name} ({self.ip_address})'

    @property
    def ip_address(self):
        return f'{self.ip_prefix}.1'
    
    @property
    def ip_prefix(self):
        ip_prefix = Setting.objects.get(name='ip_prefix').value
        return f'{ip_prefix}.{self.subnet_num}'
    
    @property
    def wg_name(self):
        return f'wgm-{self.subnet_num:03d}'
    
    @property
    def public_ip(self):
        return Setting.objects.get(name='public_ip').value
    
    def flush(self):
        return render_to_string('wireguard/conf/interface.html', {'object':self})
    
    def save_conf(self):
        conf_path = f'/etc/wireguard/{self.wg_name}.conf'
        write_to_file(conf_path, self.flush())
        

class Peer(models.Model):
    
    interface = models.ForeignKey(Interface, related_name='peers', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    description = models.TextField(null=True, blank=True)
    ip_num = models.SmallIntegerField()
    private_key = models.CharField(max_length=255)
    public_key = models.CharField(max_length=255)
    preshared_key = models.CharField(max_length=255)
    is_enabled = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('name', 'interface')
        
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.was_enabled = self.is_enabled
        
    @property
    def ip_address(self):
        ip_prefix = self.interface.ip_prefix
        return f'{ip_prefix}.{self.ip_num}'
    
    def flush(self):
        return render_to_string('wireguard/conf/peer.html', {'object': self})