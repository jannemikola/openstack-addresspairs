# Fix for OpenStack Juno bug in not being able to remove Allowed Address Pairs via GUI or CLI tools after
# adding them with CLI tool. Bug cannot be fixed by updating OpenStack CLI tools, it requires OpenStack platform
# update. This is a script to remedy the situation.
#
# Tested with HPE CloudSystem 9 OpenStack, should work with other Juno-based OpenStack variants/distributions as well.
#
# Author: Janne Mikola, janne.mikola@outlook.com

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
		
		buf = cStringIO.StringIO()
		c = pycurl.Curl()
		# No SSL Certificate verification due to our environment
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

		result = json.loads('{"access": {"token": {"issued_at": "2016-09-20T11:29:03.637166", "expires": "2016-09-20T15:29:03Z", "id": "0652079f693841e5bb48cc48ec385ca7", "tenant": {"description": "BDN-ryhm\u00e4n testi (luonut tluhtala)", "enabled": true, "id": "e2c91b59b5dc412e83e28b2705044e1e", "name": "BDN"}, "audit_ids": ["wjDpzshjR2-ShBzDOGbTXg"]}, "serviceCatalog": [{"endpoints": [{"adminURL": "http://192.168.36.98:8774/v2/e2c91b59b5dc412e83e28b2705044e1e", "region": "RegionOne", "internalURL": "http://192.168.0.1:8774/v2/e2c91b59b5dc412e83e28b2705044e1e", "id": "1f3e6e6f29364da7ae0cdb81c174aba9", "publicURL": "https://62.71.0.164:8774/v2/e2c91b59b5dc412e83e28b2705044e1e"}], "endpoints_links": [], "type": "compute", "name": "nova"}, {"endpoints": [{"adminURL": "http://192.168.36.98:9696", "region": "RegionOne", "internalURL": "http://192.168.0.1:9696", "id": "27f6067297a94c7d9cbbfdb986051e3b", "publicURL": "https://62.71.0.164:9696"}], "endpoints_links": [], "type": "network", "name": "neutron"}, {"endpoints": [{"adminURL": "http://192.168.36.98:8776/v2/e2c91b59b5dc412e83e28b2705044e1e", "region": "RegionOne", "internalURL": "http://192.168.0.1:8776/v2/e2c91b59b5dc412e83e28b2705044e1e", "id": "4dd2ed50021f4728b72f006f3ac1cf52", "publicURL": "https://62.71.0.164:8776/v2/e2c91b59b5dc412e83e28b2705044e1e"}], "endpoints_links": [], "type": "volumev2", "name": "cinderv2"}, {"endpoints": [{"adminURL": "http://62.71.0.164:9292/", "region": "RegionOne", "internalURL": "http://192.168.36.98:9292/", "id": "4d9cb09237d94b7a9c6eb21f32c6557d", "publicURL": "https://62.71.0.164:9292/"}], "endpoints_links": [], "type": "image", "name": "glance"}, {"endpoints": [{"adminURL": "http://192.168.36.98:21131/v1", "region": "RegionOne", "internalURL": "http://192.168.0.1:21131/v1", "id": "5fd4ed88708f42909f3a69c2d4eacf78", "publicURL": "https://62.71.0.164:21131/v1"}], "endpoints_links": [], "type": "hp-catalog", "name": "sherpa"}, {"endpoints": [{"adminURL": "http://192.168.36.98:8776/v1/e2c91b59b5dc412e83e28b2705044e1e", "region": "RegionOne", "internalURL": "http://192.168.0.1:8776/v1/e2c91b59b5dc412e83e28b2705044e1e", "id": "1ee1430dddbc45e79a8208d5016c0e18", "publicURL": "https://62.71.0.164:8776/v1/e2c91b59b5dc412e83e28b2705044e1e"}], "endpoints_links": [], "type": "volume", "name": "cinder"}, {"endpoints": [{"adminURL": "http://192.168.0.1:21071/1", "region": "RegionOne", "internalURL": "http://192.168.0.1:21071/1", "id": "6ea72a33ecb946adafef0367ed41cc0c", "publicURL": "http://192.168.0.1:21071/1"}], "endpoints_links": [], "type": "registry", "name": "graffiti"}, {"endpoints": [{"adminURL": "http://192.168.36.98:8004/v1/e2c91b59b5dc412e83e28b2705044e1e", "region": "RegionOne", "internalURL": "http://192.168.0.1:8004/v1/e2c91b59b5dc412e83e28b2705044e1e", "id": "55fef523123143fba4e3456bebced225", "publicURL": "https://62.71.0.164:8004/v1/e2c91b59b5dc412e83e28b2705044e1e"}], "endpoints_links": [], "type": "orchestration", "name": "heat"}, {"endpoints": [{"adminURL": "http://192.168.0.1:21051/1", "region": "RegionOne", "internalURL": "http://192.168.0.1:21051/1", "id": "0f2d06cb23f74e4abebe84b6451b8868", "publicURL": "http://192.168.0.1:21051/1"}], "endpoints_links": [], "type": "provisioner", "name": "eve"}, {"endpoints": [{"adminURL": "http://192.168.0.1:21061/1", "region": "RegionOne", "internalURL": "http://192.168.0.1:21061/1", "id": "5ca41ba0cde54450a3115b3708d00550", "publicURL": "http://192.168.0.1:21061/1"}], "endpoints_links": [], "type": "repository", "name": "focus"}, {"endpoints": [{"adminURL": "http://192.168.36.98:35357/v2.0", "region": "RegionOne", "internalURL": "http://192.168.0.1:5000/v2.0", "id": "85f2575d94bb4b0d84bd9e87657828ff", "publicURL": "https://62.71.0.164:5000/v2.0"}], "endpoints_links": [], "type": "identity", "name": "keystone"}], "user": {"username": "pwh5148", "roles_links": [], "id": "5c8a8081d9484661ad9a4508e89f2a3e", "roles": [{"name": "admin"}, {"name": "_member_"}], "name": "pwh5148"}, "metadata": {"is_admin": 0, "roles": ["42b2fa02e325403386aa48fe4145c162", "9fe2ff9ee4384b1894a90878d3e92bab"]}}}')
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
		# No SSL certificate verification enabled
            c.setopt(pycurl.SSL_VERIFYPEER, 0)
                c.setopt(pycurl.SSL_VERIFYHOST, 0)
                c.setopt(c.WRITEFUNCTION, buf.write)
                c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/json','Accept: application/json',\
				'User-Agent: python-neutronclient','X-Auth-Token: ' + self.token])
                data = json.dumps(payload)
                c.setopt(pycurl.CUSTOMREQUEST, "PUT")
                c.setopt(pycurl.POSTFIELDS, data)
                c.setopt(c.URL, url)
                c.perform()
                result = buf.getvalue()
                buf.close()

print('OpenStack Juno "Allowed Address Pairs" table clearing tool v1.0 by Janne Mikola')
print('')

ip_address = raw_input("OpenStack's IP address or FQDN: ")
username = raw_input("OpenStack username: ")
password = raw_input("OpenStack password: ")
tenant = raw_input("OpenStack tenant: ")

auth_token = Openstackauth(ip_address, username, password, tenant)
token = auth_token.request()
print('Received X-Auth token from OpenStack: ' + token)

go_on = raw_input('Continue clearing Allowed Address Pairs table? [Y/n] ')

if go_on is not "Y":
	quit()

port_uuid = raw_input("Virtual Network Interface/Port UUID: ")

Openstackfix = Openstackfix(port_uuid, token, ip_address)
Openstackfix.clear_table()

print('Table successfully cleared.')

