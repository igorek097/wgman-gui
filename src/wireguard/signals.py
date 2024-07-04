from django.db.models import signals

from wireguard import models


def interface_post_save(sender, **kwargs):
    interface = kwargs['instance']
    created = kwargs['created']
    if created:
        if interface.is_enabled:
            interface.up()
        return
    if interface.is_enabled == interface.was_enabled:
        return
    if interface.is_enabled:
        interface.up()
        return
    interface.down()


def peer_post_save(sender, **kwargs):
    peer = kwargs['instance']
    created = kwargs['created']
    if created:
        if peer.is_enabled:
            peer.interface.sync()
        return
    if peer.is_enabled == peer.was_enabled:
        return
    peer.interface.sync()
    

def interface_post_delete(sender, **kwargs):
    interface = kwargs['instance']
    if interface.is_enabled:
        interface.down()


def peer_post_delete(sender, **kwargs):
    peer = kwargs['instance']
    peer.interface.sync()


signals.post_save.connect(interface_post_save, models.Interface)
signals.post_save.connect(peer_post_save, models.Peer)

signals.post_delete.connect(interface_post_delete, models.Interface)
signals.post_delete.connect(peer_post_delete, models.Peer)

