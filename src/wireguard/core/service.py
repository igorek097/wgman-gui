from os import system, remove
from subprocess import run, PIPE
from re import sub


def syncconf(interface_name:str):
    temp_file = f'./{interface_name}-tmp.conf'
    system(f'wg-quick strip {interface_name} > {temp_file}')
    system(f'wg syncconf {interface_name} {temp_file}')
    remove(temp_file)
        

def up(interface_name:str):
    system(f'wg-quick up {interface_name}')
    

def down(interface_name:str):
    system(f'wg-quick down {interface_name}')
    

def disable(interface_name:str):
    system(f'rc-update del wg-quick@{interface_name}')
    

def enable(interface_name:str):
    system(f'rc-update add wg-quick@{interface_name} default')
    

def is_active(interface_name:str):
    lookup_str = f'interface: {interface_name}'
    wg_status = run(['wg'], stdout=PIPE).stdout.decode()
    return lookup_str in wg_status

def peer_last_seen(peer_ip):
    wg_status = run(['wg'], stdout=PIPE).stdout.decode()
    status = [s.strip() for s in wg_status.split('\n')]
    search_str = f'allowed ips: {peer_ip}/32'
    try:
        idx = status.index(search_str)
    except:
        return None
    if 'latest handshake' in status[idx+1]:
        timestr = status[idx+1].replace('latest handshake: ', '')
        timestr = sub(r'minutes|minute', 'm', timestr)
        timestr = sub(r'seconds|second', 's', timestr)
        timestr = timestr.replace(' ', '').replace(',', '')
        return timestr
    return None