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
