from jinja2 import Template

centos_eth = Template('''
DEVICE={{ device }}

IPADDR={{ ip4 }}
NETMASK={{ netmask4 }}

{% if gatteway4 %}
DEFROUTE=yes
GATEWAY={{ gateway4 }}
{% endif %}

ONBOOT=yes
BOOTPROTO=none
USERCTL=no
NM_CONTROLLED=no
''')


centos_bond_eth = Template('''
TYPE="Ethernet"
BOOTPROTO="none"
PEERDNS="yes"
PEERROUTES="yes"
IPV4_FAILURE_FATAL="no"
DEVICE={{ device }}
ONBOOT="yes"
MASTER={{ bond }}
SLAVE=yes
''')

centos_bond_master = Template('''
DEVICE=bond0
NAME=bond0
TYPE=Bond
BONDING_MASTER=yes
IPADDR={{ ip4 }}
NETMASK={{ netmask4 }}
ONBOOT=yes
BOOTPROTO=none
BONDING_OPTS="mode={{ mode }} miimon=100"

{% if gatteway4 %}
DEFROUTE=yes
GATEWAY={{ gateway4 }}
{% endif %}
''')

ubuntu_eth = Template('''
iface {{ device }} inet static
    address {{ ip4 }}
    netmask {{ netmask4 }}
    gateway {{ gateway4 }}
''')
