# =========================================================================
# twr-01 — MikroTik CHR (RouterOS v7)
# Role: Tower / Edge VTEP
# Router ID: 100.127.50.101
# AS: 4208675309
# =========================================================================

/system identity
set name=twr-01.sa51.dev
/system note
set show-at-login=no

# -------------------------------------------------------------------------
# Interfaces — Bridge, Loopbacks, Ethernet
# -------------------------------------------------------------------------

/interface bridge
add name=br-router vlan-filtering=yes
add name=lo.4
add name=lo.6

/interface ethernet
set [ find default-name=ether1 ] disable-running-check=no
set [ find default-name=ether2 ] disable-running-check=no
set [ find default-name=ether3 ] disable-running-check=no
set [ find default-name=ether4 ] disable-running-check=no
set [ find default-name=ether5 ] disable-running-check=no
set [ find default-name=ether6 ] disable-running-check=no
set [ find default-name=ether7 ] disable-running-check=no
set [ find default-name=ether8 ] disable-running-check=no

# -------------------------------------------------------------------------
# VXLAN Interfaces
# -------------------------------------------------------------------------

/interface vxlan
add bridge=br-router bridge-pvid=1104 learning=no \
    local-address=100.127.50.101 \
    mac-address=72:F8:A7:93:B5:43 \
    name=vxlan-1104-ipv4-twr-01 vni=1104
add bridge=br-router bridge-pvid=1106 learning=no \
    local-address=3fff:1ab:d127:d50::101 \
    mac-address=0E:2C:97:B8:5F:8D \
    name=vxlan-1106-ipv6-twr-01 vni=1106 vteps-ip-version=ipv6

# -------------------------------------------------------------------------
# VLANs
# -------------------------------------------------------------------------

/interface vlan
add interface=br-router name=v1104 vlan-id=1104
add interface=br-router name=v1106 vlan-id=1106

/interface bridge vlan
add bridge=br-router tagged=br-router vlan-ids=1104
add bridge=br-router tagged=br-router vlan-ids=1106

# -------------------------------------------------------------------------
# VRF — Lab Management
# -------------------------------------------------------------------------

/ip vrf
add interfaces=ether1 name=vrf-lab-mgmt

# -------------------------------------------------------------------------
# Port
# -------------------------------------------------------------------------

/port
set 0 name=serial0

# -------------------------------------------------------------------------
# IPv4 Addressing
# -------------------------------------------------------------------------

/ip address
add address=100.126.50.2/29 interface=ether2 network=100.126.50.0
add address=100.126.50.9/29 interface=ether3 network=100.126.50.8
add address=100.127.50.101 interface=lo.4 network=100.127.50.101
add address=198.18.104.101/24 interface=v1104 network=198.18.104.0
add address=198.18.106.101/24 interface=v1106 network=198.18.106.0

# -------------------------------------------------------------------------
# IPv6 Addressing
# -------------------------------------------------------------------------

/ipv6 settings
set accept-router-advertisements=yes

/ipv6 address
add address=3fff:1ab:d127:d50::101/128 advertise=no interface=lo.6
add address=3fff:1ab:d50:d0::2/64 advertise=no interface=ether2
add address=3fff:1ab:d50:d8::9/64 advertise=no interface=ether3

# -------------------------------------------------------------------------
# Management — Static IP
# -------------------------------------------------------------------------

/ip address
add address=172.31.1.13/24 interface=ether1 network=172.31.1.0
/ip route
add dst-address=0.0.0.0/0 gateway=172.31.1.1 routing-table=vrf-lab-mgmt

# -------------------------------------------------------------------------
# Services — Restrict to Management VRF
# -------------------------------------------------------------------------

/ip service
set ssh vrf=vrf-lab-mgmt
set winbox vrf=vrf-lab-mgmt

/ipv6 route
add gateway=3fff:da7a:1ab:77::1 routing-table=vrf-lab-mgmt vrf-interface=vrf-lab-mgmt

# -------------------------------------------------------------------------
# Routing ID
# -------------------------------------------------------------------------

/routing id
add disabled=no id=100.127.50.101 name=id-main select-dynamic-id=""

# -------------------------------------------------------------------------
# IS-IS Underlay
# -------------------------------------------------------------------------

/routing isis instance
add afi=ip,ipv6 areas=49.0051 l2.originate-default=never \
    name=ipvx-isis-1 system-id=1001.2705.0101

/routing isis interface-template
add instance=ipvx-isis-1 interfaces=lo.4 levels=l2
add instance=ipvx-isis-1 interfaces=lo.6 levels=l2
add instance=ipvx-isis-1 interfaces=ether1 levels=l2
add instance=ipvx-isis-1 interfaces=ether2 levels=l2
add instance=ipvx-isis-1 interfaces=ether3 levels=l2
add instance=ipvx-isis-1 interfaces=ether4 levels=l2

# -------------------------------------------------------------------------
# BGP Instance & Templates
# -------------------------------------------------------------------------

/routing bgp instance
add as=4208675309 name=bgp-instance-as4208675309-01 router-id=100.127.50.101

/routing bgp template
add afi=ip as=4208675309 hold-time=15s keepalive-time=5s \
    name=bgp-tmplt-ipv4-as4208675309
add afi=ipv6 as=4208675309 hold-time=15s keepalive-time=5s \
    name=bgp-tmplt-ipv6-as4208675309

# -------------------------------------------------------------------------
# BGP Connections — Peers to core-01 (Route Reflector)
# -------------------------------------------------------------------------

/routing bgp connection
add afi=ip,evpn disabled=no \
    instance=bgp-instance-as4208675309-01 \
    local.address=100.127.50.101 .role=ibgp \
    name=bgp-peer-ipv4-core-01 \
    remote.address=100.127.1.1 .as=4208675309 \
    templates=bgp-tmplt-ipv4-as4208675309
add afi=ipv6,evpn \
    instance=bgp-instance-as4208675309-01 \
    local.address=3fff:1ab:d127:d50::101 .role=ibgp \
    name=bgp-peer-ipv6-core-01 \
    remote.address=3fff:1ab:d127:d1::1 .as=4208675309 \
    templates=bgp-tmplt-ipv6-as4208675309

# -------------------------------------------------------------------------
# BGP EVPN — VNI Bindings
# -------------------------------------------------------------------------

/routing bgp evpn
add export.route-targets=1104:1104 import.route-targets=1104:1104 \
    instance=bgp-instance-as4208675309-01 \
    name=bgp-evpn-ipv4-vni1104 vni=1104
add export.route-targets=1106:1106 import.route-targets=1106:1106 \
    instance=bgp-instance-as4208675309-01 \
    name=bgp-evpn-ipv6-vni1106 vni=1106

# -------------------------------------------------------------------------
# Tools
# -------------------------------------------------------------------------

/tool romon
set enabled=yes
/tool sniffer
set file-limit=10000KiB file-name=bgp-twr-01 \
    filter-ip-protocol=tcp filter-port=bgp
