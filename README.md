# openstack-addresspairs
Workaround for OpenStack bug in Juno and Kilo releases, where user is not able to remove allowed_address_pairs via GUI (Horizon) nor CLI after adding them with command-line client. This bug cannot be fixed by updating OpenStack CLI tools, it requires OpenStack platform upgrade, and such a thing can be impossible depending on your role in the system (e.g. if you are just a tenant). This is a script to remedy the situation by utilizing OpenStack's RESTful API, which is the only known workaround.

Tested with HPE CloudSystem 9 OpenStack (Juno), should work with other Juno-based OpenStack variants/distributions as well. Kilo compatibility unknown, but will verify and make the script adaptive for different versions later.

The bug is documented in e.g. here: http://lists.openstack.org/pipermail/openstack-dev/2015-September/075636.html and here: https://bugs.launchpad.net/juniperopenstack/+bug/1351979

Author: Janne Mikola, janne.mikola@outlook.com

Needed dependency: pycurl ("sudo apt-get install python-pycurl")


