# username: Proxmox user (default: root)
# key: The API Token or password

nodes = {
    # AkaliCA
    '144.217.10.65': {
        'username': 'root',
        'key': 'V%ui*Vp6YcDDfV'
    },

    # AsheCA
    '144.217.10.80': {
        'username': 'root',
        'key': 'vZ%ex%ZJlgP3'
    },

    # UniversCA
    '54.39.131.128': {
        'username': 'root',
        'key': 'Z2j$L8eLQ2SS'
    }
}

def get_vm_info(datacenter, node, vm_id):
    try:
        return datacenter.nodes(node['node']).qemu(vm_id).status.current.get()
    
    except Exception as e:
        pass

    try:
        return datacenter.nodes(node['node']).lxc(vm_id).status.current.get()
    
    except Exception as e:
        pass

    return None