from django.db.models import signals

from wireguard import models
from wireguard.core import service


def interface_post_save(sender, **kwargs):
    interface = kwargs['instance']
    created = kwargs['created']
    if created:
        if interface.is_enabled:
            interface.save_conf()
            service.up(interface.wg_name)
        return
    if interface.is_enabled == interface.was_enabled:
        return
    if interface.is_enabled:
        interface.save_conf()
        service.up(interface.wg_name)
        return
    service.down(interface.wg_name)


def peer_post_save(sender, **kwargs):
    peer = kwargs['instance']
    created = kwargs['created']
    if created:
        if peer.is_enabled:
            peer.interface.save_conf()
            service.syncconf(peer.interface.wg_name)
        return
    if peer.is_enabled == peer.was_enabled:
        return
    peer.interface.save_conf()
    service.syncconf(peer.interface.wg_name)
    

signals.post_save.connect(interface_post_save, models.Interface)
signals.post_save.connect(peer_post_save, models.Peer)

