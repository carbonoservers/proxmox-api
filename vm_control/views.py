# Flask
from flask import Blueprint, request, abort, jsonify

# Modules
from proxmox import ProxmoxAPI
from utils import auth
from utils import datacenters

# Register blueprint
vm_control = Blueprint('vm_control', __name__)

# Get usage
@vm_control.route('/vm/<datacenter_addr>/<vm_id>', methods = ['GET', 'POST'])
def vm_usage(datacenter_addr, vm_id):
	auth.check_key(request)

	credentials = datacenters.nodes.get(datacenter_addr)
	if not credentials:
		abort(404, description = "This datacenter does not exist")

	try:
		datacenter = ProxmoxAPI(
			f'{ datacenter_addr }:8006',
			user = f'{ credentials.get("username") }@pam',
			password = credentials.get("key"),
			verify_ssl = False
		)

		vm_info = None
		for node in datacenter.nodes.get():
			vm_info = datacenters.get_vm_info(datacenter, node, vm_id)
			break

		if not vm_info:
			abort(404, description = "This vm does not exist")
		
		netin = 0
		netout = 0

		try:
			if vm_info.get('nics'):
				for interface in vm_info['nics']:
					netin = int( vm_info['nics'][interface].get('netin') )
					netout = int( vm_info['nics'][interface].get('netout') )
			else:
				netin = int( vm_info.get('netin') )
				netout = int( vm_info.get('netout') )
		
		except:
			netin = 0
			netout = 0
			pass

		return jsonify(
			cpu = str( round(vm_info['cpu'], 1) ),
			ram = str( round( (vm_info['mem'] / vm_info['maxmem']) * 100, 1) ),
			inkbps = str( round((netin / (1024 * 4 * 4)) / 1024) ),
			outkbps = str( round((netout / (1024 * 4 * 4)) / 1024) ),
			status = vm_info['status']
		)
	
	except Exception as e:
		abort(500, description = e)
	
	return jsonify()
