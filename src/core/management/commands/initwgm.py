from os import system, getenv, path
from subprocess import run, PIPE

from django.core.management.base import BaseCommand
from django.conf import settings

from core.models import Setting
from wireguard.models import Interface


class Command(BaseCommand):
    
    help = 'Initialize Application on container start'
    
    def handle(self, *args, **options):
        if not path.exists(settings.DB_PATH):
            db_dir = path.dirname(settings.DB_PATH)
            if not path.exists(db_dir):
                system(f'mkdir {db_dir}')
            self.migrate()
            Setting(name='public_ip', value=self.get_public_ip()).save()
            Setting(name='ip_prefix', value=self.get_ip_prefix()).save()
            return
        self.migrate()
        for net in Interface.objects.filter(is_enabled=True):
            net.up()
            
    def migrate(self):
        system(f'python {settings.BASE_DIR}/manage.py migrate')
    
    def get_public_ip(self):
        public_ip = getenv('PUBLIC_IP')
        if not public_ip:
            command = run(['curl', '2ip.io'], stdout=PIPE)
            public_ip = command.stdout.decode().replace('\n', '')
        return public_ip
    
    def get_ip_prefix(self):
        return getenv('IP_PREFIX') or '10.22'