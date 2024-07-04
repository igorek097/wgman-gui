from os import remove, system
from re import sub

from django.db import models
from django.template.loader import render_to_string

from core.models import Setting
from core.tools import write_to_file
from wireguard.core import service


class Interface(models.Model):
    
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)
    subnet_num = models.SmallIntegerField()
    listen_port = models.PositiveIntegerField(unique=True)
    private_key = models.CharField(max_length=255)
    public_key = models.CharField(max_length=255)
    is_enabled = models.BooleanField(default=True)
    dns = models.CharField(max_length=15, blank=True, null=True)
    
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
    def netmask(self):
        return f'{self.ip_prefix}.0/24'
    
    @property
    def wg_name(self):
        return f'wgm-{self.subnet_num:03d}'
    
    @property
    def public_ip(self):
        return Setting.objects.get(name='public_ip').value
    
    def flush(self):
        return render_to_string('wireguard/conf/interface.html', {'object':self})
    
    def save_conf(self):
        write_to_file(self.get_conf_filename(), self.flush())
        
    def delete_conf(self):
        remove(self.get_conf_filename())
        
    def up(self):
        self.iptables('up')
        self.save_conf()
        service.up(self.wg_name)
        
    def down(self):
        service.down(self.wg_name)
        self.iptables('down')
        self.delete_conf()
        
    def sync(self):
        self.save_conf()
        service.syncconf(self.wg_name)
        
    @property
    def is_active(self):
        return service.is_active(self.wg_name)
    
    def get_conf_filename(self):
        return f'/etc/wireguard/{self.wg_name}.conf'

    def iptables(self, action:str):
        if not action in ['up', 'down']:
            action = 'down'
        for rule in self.get_ip_rules():
            if action == 'down':
                rule = sub(r'-A|-I', '-D', rule)
            system(rule)
            
    def get_ip_rules(self):
        return [
            f'iptables -I FORWARD -s {self.netmask} -j ACCEPT',
        ]
        

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
    
    @property
    def last_seen(self):
        return service.peer_last_seen(self.ip_address)

    def flush(self):
        return render_to_string('wireguard/conf/peer.html', {'object': self})