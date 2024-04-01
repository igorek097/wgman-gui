def get_vacant_address(existing_range):
    addr_range = list(range(1, 255))
    return get_vacants(addr_range, existing_range)[0]


def get_vacant_port(existing_range):
    port_range = list(range(51820, 51920))
    return get_vacants(port_range, existing_range)[0]
        

def get_vacants(initial_range, occupied_range):
    for i in occupied_range:
        initial_range.remove(i)
    return initial_range