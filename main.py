# Workaround for OpenStack bug in Juno and Kilo releases, where user is not able to remove allowed_address_pairs via GUI 
# (Horizon) nor CLI after adding them with command-line client. This bug cannot be fixed by updating OpenStack CLI tools, it 
# requires OpenStack platform upgrade, and such a thing can be impossible depending on your role in the system (e.g. if you 
# are just a tenant). This is a script to remedy the situation by utilizing OpenStack's RESTful API, which is the only known 
# workaround.
#
# Tested with HPE CloudSystem 9 OpenStack (Juno), should work with other Juno-based OpenStack variants/distributions as well. Kilo 
# compatibility unknown, but will verify and make the script adaptive for different versions later.
#
# The bug is documented in e.g. here: http://lists.openstack.org/pipermail/openstack-dev/2015-September/075636.html and
# here: https://bugs.launchpad.net/juniperopenstack/+bug/1351979
#
# Author: Janne Mikola, janne.mikola@outlook.com

# Needed dependency: pycurl ("sudo apt-get install python-pycurl")
import pycurl
import cStringIO 
import json

class Openstackauth:
	# Class for getting an auth token from OpenStack API
	def __init__(self, ip_address, username, password, tenant):
		self.ip_address = ip_address
		self.username = username
		self.password = password
		self.tenant = tenant

	def request(self):
		url = 'https://' + self.ip_address + ':5000/v2.0/tokens'
		payload = '{"auth": {"tenantName": "' + self.tenant + \
			'", "passwordCredentials": {"username": "' + self.username + \
			'", "password": "' + self.password + '"}}}'
		print('Attempting to get authentication token from ' + url + ' with the following credentials: ' + payload)
		
		# Saving pycurl output to buf instead of stdout.
		buf = cStringIO.StringIO()
		c = pycurl.Curl()
		# No SSL Certificate verification due to our environment. Change to '1' to secure environments.
		c.setopt(pycurl.SSL_VERIFYPEER, 0)   
		c.setopt(pycurl.SSL_VERIFYHOST, 0)
		c.setopt(c.WRITEFUNCTION, buf.write)
		c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/json','Accept: application/json'])
		data = json.dumps(payload)
		c.setopt(pycurl.POST, 1)
		c.setopt(pycurl.POSTFIELDS, data)
		c.setopt(c.URL, url)
		c.perform()
		result = buf.getvalue()
		buf.close()
		# Navigate the X-Auth-Token from the reply
		tokenkey = result['access']['token']['id']
		return tokenkey

class Openstackfix:
	# Class for clearing Allowed Address Pairs for one Virtual Port at a time
	def __init__(self, port, token, ip_address):
		self.port = port
		self.token = token
		self.ip_address = ip_address

	def clear_table(self):
		url = 'https://' + self.ip_address + ':9696/v2.0/ports/' + self.port + '.json'
                payload = '{"port": {"allowed_address_pairs": []}}'

		buf = cStringIO.StringIO()
                c = pycurl.Curl()
		# To enable SSL Certificate verification change to '1'
            	c.setopt(pycurl.SSL_VERIFYPEER, 0)
                c.setopt(pycurl.SSL_VERIFYHOST, 0)
                c.setopt(c.WRITEFUNCTION, buf.write)
                c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/json','Accept: application/json',\
				'User-Agent: python-neutronclient','X-Auth-Token: ' + self.token])
                data = json.dumps(payload)
		# HTTP PUT works a bit wonkily with pycurl; use CUSTOMREQUEST and POSTFIELDS.
                c.setopt(pycurl.CUSTOMREQUEST, "PUT")
                c.setopt(pycurl.POSTFIELDS, data)
                c.setopt(c.URL, url)
                c.perform()
                result = buf.getvalue()
                buf.close()
		return True

print('OpenStack Juno/Kilo "allowed_address_pairs"-table clearing tool v1.0 by Janne Mikola (janne.mikola@outlook.com)')
print('')

ip_address = raw_input("OpenStack's IP address or FQDN: ")
username = raw_input("OpenStack username: ")
password = raw_input("OpenStack password: ")
tenant = raw_input("OpenStack tenant: ")

# Get auth token
Openstackauth = Openstackauth(ip_address, username, password, tenant)
token = Openstackauth.request()
print('Received X-Auth-Token from OpenStack: ' + token)
print('')
write_changes = raw_input('Continue clearing Allowed Address Pairs table? [Y/n] ')

if write_changes is not "Y":
	quit()

port_uuid = raw_input("Virtual Network Interface/Port UUID: ")

# Clear the table of given Port UUID
Openstackfix = Openstackfix(port_uuid, token, ip_address)
success = Openstackfix.clear_table()

if success == True:
	print('Table successfully cleared.')
