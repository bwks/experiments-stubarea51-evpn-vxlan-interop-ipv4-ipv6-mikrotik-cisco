"""Expected values for all test cases, derived from the test plan."""

# ============================================================================
# Section 1: Physical / Link Layer
# ============================================================================

INTERFACE_STATE_CHECKS = [
    # (test_id, device, interface, device_type)
    ("1.1.1", "core-01", "GigabitEthernet2", "ios"),
    ("1.1.2", "agg-01", "GigabitEthernet5", "ios"),
    ("1.1.3", "agg-01", "GigabitEthernet2", "ios"),
    ("1.1.4", "agg-01", "GigabitEthernet3", "ios"),
    ("1.1.5", "twr-01", "ether2", "mk"),
    ("1.1.6", "twr-01", "ether3", "mk"),
    ("1.1.7", "twr-02", "ether2", "mk"),
    ("1.1.8", "twr-02", "ether3", "mk"),
    ("1.1.9", "twr-03", "ether2", "mk"),
    ("1.1.10", "twr-03", "ether3", "mk"),
]

MTU_CHECKS = [
    # (test_id, device, interfaces, device_type)
    ("1.2.1", "core-01", ["GigabitEthernet2"], "ios"),
    ("1.2.2", "agg-01", ["GigabitEthernet2", "GigabitEthernet3", "GigabitEthernet5"], "ios"),
    ("1.2.3", "twr-01", ["ether2", "ether3"], "mk"),
    ("1.2.4", "twr-02", ["ether2", "ether3"], "mk"),
    ("1.2.5", "twr-03", ["ether2", "ether3"], "mk"),
]

# ============================================================================
# Section 2: IP Addressing
# ============================================================================

IPV4_LINK_ADDRESSES = [
    # (test_id, device, interface, expected_address, device_type)
    ("2.1.1", "core-01", "GigabitEthernet2", "100.126.1.49", "ios"),
    ("2.1.2", "agg-01", "GigabitEthernet5", "100.126.1.50", "ios"),
    ("2.1.3", "agg-01", "GigabitEthernet2", "100.126.50.1", "ios"),
    ("2.1.4", "agg-01", "GigabitEthernet3", "100.126.50.17", "ios"),
    ("2.1.5", "twr-01", "ether2", "100.126.50.2", "mk"),
    ("2.1.6", "twr-01", "ether3", "100.126.50.9", "mk"),
    ("2.1.7", "twr-02", "ether2", "100.126.50.18", "mk"),
    ("2.1.8", "twr-02", "ether3", "100.126.50.25", "mk"),
    ("2.1.9", "twr-03", "ether2", "100.126.50.10", "mk"),
    ("2.1.10", "twr-03", "ether3", "100.126.50.26", "mk"),
]

IPV6_LINK_ADDRESSES = [
    # (test_id, device, interface, expected_address, device_type)
    ("2.2.1", "core-01", "GigabitEthernet2", "3fff:1ab:d1:d48::49", "ios"),
    ("2.2.2", "agg-01", "GigabitEthernet5", "3fff:1ab:d1:d48::50", "ios"),
    ("2.2.3", "agg-01", "GigabitEthernet2", "3fff:1ab:d50:d0::1", "ios"),
    ("2.2.4", "agg-01", "GigabitEthernet3", "3fff:1ab:d50:d16::d17", "ios"),
    ("2.2.5", "twr-01", "ether2", "3fff:1ab:d50:d0::2", "mk"),
    ("2.2.6", "twr-01", "ether3", "3fff:1ab:d50:d8::9", "mk"),
    ("2.2.7", "twr-02", "ether2", "3fff:1ab:d50:d16::d18", "mk"),
    ("2.2.8", "twr-02", "ether3", "3fff:1ab:d50:d24::d25", "mk"),
    ("2.2.9", "twr-03", "ether2", "3fff:1ab:d50:d8::10", "mk"),
    ("2.2.10", "twr-03", "ether3", "3fff:1ab:d50:d24::26", "mk"),
]

LOOPBACK_ADDRESSES = [
    # (test_id, device, ipv4, ipv6, device_type)
    ("2.3.1", "core-01", "100.127.1.1", "3fff:1ab:d127:d1::1", "ios"),
    ("2.3.2", "agg-01", "100.127.1.21", "3fff:1ab:d127:d1::21", "ios"),
    ("2.3.3", "twr-01", "100.127.50.101", "3fff:1ab:d127:d50::101", "mk"),
    ("2.3.4", "twr-02", "100.127.50.102", "3fff:1ab:d127:d50::102", "mk"),
    ("2.3.5", "twr-03", "100.127.50.103", "3fff:1ab:d127:d50::103", "mk"),
]

PING_TESTS_IPV4_LINK = [
    # (test_id, src_device, target_ip, device_type)
    ("2.4.1", "core-01", "100.126.1.50", "ios"),
    ("2.4.2", "agg-01", "100.126.1.49", "ios"),
    ("2.4.3", "agg-01", "100.126.50.2", "ios"),
    ("2.4.4", "agg-01", "100.126.50.18", "ios"),
    ("2.4.5", "twr-01", "100.126.50.10", "mk"),
    ("2.4.6", "twr-02", "100.126.50.26", "mk"),
]

PING_TESTS_IPV6_LINK = [
    # (test_id, src_device, target_ip, device_type)
    ("2.5.1", "core-01", "3fff:1ab:d1:d48::50", "ios"),
    ("2.5.2", "agg-01", "3fff:1ab:d1:d48::49", "ios"),
    ("2.5.3", "agg-01", "3fff:1ab:d50:d0::2", "ios"),
    ("2.5.4", "agg-01", "3fff:1ab:d50:d16::d18", "ios"),
    ("2.5.5", "twr-01", "3fff:1ab:d50:d8::10", "mk"),
    ("2.5.6", "twr-02", "3fff:1ab:d50:d24::26", "mk"),
]

# ============================================================================
# Section 3: IS-IS Underlay
# ============================================================================

ISIS_NEIGHBORS = [
    # (test_id, device, neighbor_name_or_sysid, interface, device_type)
    ("3.1.1", "core-01", "agg-01", "Gig2", "ios"),
    ("3.1.2", "agg-01", "core-01", "Gig5", "ios"),
    ("3.1.3", "agg-01", "1001.2705.0101", "Gig2", "ios"),  # twr-01 by system-id
    ("3.1.4", "agg-01", "1001.2705.0102", "Gig3", "ios"),  # twr-02 by system-id
    ("3.1.5", "twr-01", "1001.2700.1021", "ether2", "mk"),  # agg-01 system-id
    ("3.1.6", "twr-01", "1001.2705.0103", "ether3", "mk"),  # twr-03 system-id
    ("3.1.7", "twr-02", "1001.2700.1021", "ether2", "mk"),  # agg-01 system-id
    ("3.1.8", "twr-02", "1001.2705.0103", "ether3", "mk"),  # twr-03 system-id
    ("3.1.9", "twr-03", "1001.2705.0101", "ether2", "mk"),  # twr-01 system-id
    ("3.1.10", "twr-03", "1001.2705.0102", "ether3", "mk"),  # twr-02 system-id
]

ISIS_INSTANCE_PARAMS = [
    # (test_id, device, parameter_desc, expected_value, device_type)
    ("3.2.1", "core-01", "area", "49.0051", "ios"),
    ("3.2.2", "core-01", "System Id", "1001.2700.1001", "ios"),
    ("3.2.3", "core-01", "IS-Type", "level-2", "ios"),
    ("3.2.4", "core-01", "Metric style", "wide", "ios"),
    ("3.2.5", "agg-01", "System Id", "1001.2700.1021", "ios"),
    ("3.2.6", "twr-01", "System ID", "1001.2705.0101", "mk"),
    ("3.2.7", "twr-02", "System ID", "1001.2705.0102", "mk"),
    ("3.2.8", "twr-03", "System ID", "1001.2705.0103", "mk"),
]

ISIS_IPV4_ROUTES = [
    # (test_id, device, expected_route_prefix, device_type)
    ("3.3.1", "core-01", "100.127.1.21", "ios"),
    ("3.3.2", "core-01", "100.127.50.101", "ios"),
    ("3.3.3", "core-01", "100.127.50.102", "ios"),
    ("3.3.4", "core-01", "100.127.50.103", "ios"),
    ("3.3.5", "agg-01", "100.127.1.1", "ios"),
    ("3.3.6", "agg-01", "100.127.50.101", "ios"),
    ("3.3.7", "agg-01", "100.127.50.102", "ios"),
    ("3.3.8", "agg-01", "100.127.50.103", "ios"),
    ("3.3.9", "twr-01", "100.127.1.1", "mk"),
    ("3.3.10", "twr-01", "100.127.1.21", "mk"),
    ("3.3.11", "twr-01", "100.127.50.102", "mk"),
    ("3.3.12", "twr-01", "100.127.50.103", "mk"),
    ("3.3.13", "twr-02", "100.127.1.1", "mk"),
    ("3.3.14", "twr-02", "100.127.1.21", "mk"),
    ("3.3.15", "twr-02", "100.127.50.101", "mk"),
    ("3.3.16", "twr-02", "100.127.50.103", "mk"),
    ("3.3.17", "twr-03", "100.127.1.1", "mk"),
    ("3.3.18", "twr-03", "100.127.1.21", "mk"),
    ("3.3.19", "twr-03", "100.127.50.101", "mk"),
    ("3.3.20", "twr-03", "100.127.50.102", "mk"),
]

ISIS_IPV6_ROUTES = [
    # (test_id, device, expected_route_prefix, device_type)
    ("3.4.1", "core-01", "3FFF:1AB:D127:D1::21", "ios"),
    ("3.4.2", "core-01", "3FFF:1AB:D127:D50::101", "ios"),
    ("3.4.3", "core-01", "3FFF:1AB:D127:D50::102", "ios"),
    ("3.4.4", "core-01", "3FFF:1AB:D127:D50::103", "ios"),
    ("3.4.5", "twr-01", "3fff:1ab:d127:d1::1", "mk"),
    ("3.4.6", "twr-02", "3fff:1ab:d127:d1::1", "mk"),
    ("3.4.7", "twr-03", "3fff:1ab:d127:d1::1", "mk"),
]

PING_TESTS_LOOPBACK_IPV4 = [
    # (test_id, src_device, target_ip)
    ("3.5.1", "twr-01", "100.127.1.1"),
    ("3.5.2", "twr-02", "100.127.1.1"),
    ("3.5.3", "twr-03", "100.127.1.1"),
    ("3.5.4", "twr-01", "100.127.50.102"),
    ("3.5.5", "twr-01", "100.127.50.103"),
    ("3.5.6", "twr-02", "100.127.50.103"),
]

PING_TESTS_LOOPBACK_IPV6 = [
    # (test_id, src_device, target_ip)
    ("3.6.1", "twr-01", "3fff:1ab:d127:d1::1"),
    ("3.6.2", "twr-02", "3fff:1ab:d127:d1::1"),
    ("3.6.3", "twr-03", "3fff:1ab:d127:d1::1"),
    ("3.6.4", "twr-01", "3fff:1ab:d127:d50::102"),
    ("3.6.5", "twr-01", "3fff:1ab:d127:d50::103"),
    ("3.6.6", "twr-02", "3fff:1ab:d127:d50::103"),
]

# ============================================================================
# Section 4: BGP Control Plane
# ============================================================================

BGP_SESSIONS_IOS = [
    # (test_id, device, neighbor_ip, transport, verify_cmd)
    ("4.1.1", "core-01", "100.127.50.101", "IPv4", "show bgp summary"),
    ("4.1.2", "core-01", "100.127.50.102", "IPv4", "show bgp summary"),
    ("4.1.3", "core-01", "100.127.50.103", "IPv4", "show bgp summary"),
    ("4.1.4", "core-01", "3FFF:1AB:D127:D50::101", "IPv6", "show bgp ipv6 unicast summary"),
    ("4.1.5", "core-01", "3FFF:1AB:D127:D50::102", "IPv6", "show bgp ipv6 unicast summary"),
    ("4.1.6", "core-01", "3FFF:1AB:D127:D50::103", "IPv6", "show bgp ipv6 unicast summary"),
]

BGP_SESSIONS_MK = [
    # (test_id, device, neighbor_ip, transport)
    ("4.1.7", "twr-01", "100.127.1.1", "IPv4"),
    ("4.1.8", "twr-01", "3fff:1ab:d127:d1::1", "IPv6"),
    ("4.1.9", "twr-02", "100.127.1.1", "IPv4"),
    ("4.1.10", "twr-02", "3fff:1ab:d127:d1::1", "IPv6"),
    ("4.1.11", "twr-03", "100.127.1.1", "IPv4"),
    ("4.1.12", "twr-03", "3fff:1ab:d127:d1::1", "IPv6"),
]

# ============================================================================
# Section 5: EVPN Control Plane
# ============================================================================

EVPN_TYPE3_ORIGINATION = [
    # (test_id, originator, vni, vtep_address)
    ("5.1.1", "twr-01", 1104, "100.127.50.101"),
    ("5.1.2", "twr-01", 1106, "3fff:1ab:d127:d50::101"),
    ("5.1.3", "twr-02", 1104, "100.127.50.102"),
    ("5.1.4", "twr-02", 1106, "3fff:1ab:d127:d50::102"),
    ("5.1.5", "twr-03", 1104, "100.127.50.103"),
    ("5.1.6", "twr-03", 1106, "3fff:1ab:d127:d50::103"),
]

EVPN_ROUTE_TARGETS = [
    # (test_id, device, vni, rt)
    ("5.3.1", "twr-01", 1104, "1104:1104"),
    ("5.3.2", "twr-01", 1106, "1106:1106"),
]

# ============================================================================
# Section 6: VXLAN Data Plane
# ============================================================================

VXLAN_INTERFACES = [
    # (test_id, device, vni, local_address, learning)
    ("6.1.1", "twr-01", 1104, "100.127.50.101", "no"),
    ("6.1.2", "twr-01", 1106, "3fff:1ab:d127:d50::101", "no"),
    ("6.1.3", "twr-02", 1104, "100.127.50.102", "no"),
    ("6.1.4", "twr-02", 1106, "3fff:1ab:d127:d50::102", "no"),
    ("6.1.5", "twr-03", 1104, "100.127.50.103", "no"),
    ("6.1.6", "twr-03", 1106, "3fff:1ab:d127:d50::103", "no"),
]

VTEP_DISCOVERY = [
    # (test_id, device, vni, expected_remote_vteps)
    ("6.2.1", "twr-01", 1104, ["100.127.50.102", "100.127.50.103"]),
    ("6.2.2", "twr-01", 1106, ["3fff:1ab:d127:d50::102", "3fff:1ab:d127:d50::103"]),
    ("6.2.3", "twr-02", 1104, ["100.127.50.101", "100.127.50.103"]),
    ("6.2.4", "twr-02", 1106, ["3fff:1ab:d127:d50::101", "3fff:1ab:d127:d50::103"]),
    ("6.2.5", "twr-03", 1104, ["100.127.50.101", "100.127.50.102"]),
    ("6.2.6", "twr-03", 1106, ["3fff:1ab:d127:d50::101", "3fff:1ab:d127:d50::102"]),
]

BRIDGE_VLAN_BINDINGS = [
    # (test_id, device, vxlan_interface_fragment, pvid)
    ("6.3.1", "twr-01", "vxlan-1104", "1104"),
    ("6.3.2", "twr-01", "vxlan-1106", "1106"),
    ("6.3.3", "twr-02", "vxlan-1104", "1104"),
    ("6.3.4", "twr-02", "vxlan-1106", "1106"),
    ("6.3.5", "twr-03", "vxlan-1104", "1104"),
    ("6.3.6", "twr-03", "vxlan-1106", "1106"),
]

# ============================================================================
# Section 7: Overlay Connectivity
# ============================================================================

PING_TESTS_VNI1104 = [
    # (test_id, src_device, src_ip, target_ip)
    ("7.1.1", "twr-01", "198.18.104.101", "198.18.104.102"),
    ("7.1.2", "twr-01", "198.18.104.101", "198.18.104.103"),
    ("7.1.3", "twr-02", "198.18.104.102", "198.18.104.101"),
    ("7.1.4", "twr-02", "198.18.104.102", "198.18.104.103"),
    ("7.1.5", "twr-03", "198.18.104.103", "198.18.104.101"),
    ("7.1.6", "twr-03", "198.18.104.103", "198.18.104.102"),
]

PING_TESTS_VNI1106 = [
    # (test_id, src_device, src_ip, target_ip)
    ("7.2.1", "twr-01", "198.18.106.101", "198.18.106.102"),
    ("7.2.2", "twr-01", "198.18.106.101", "198.18.106.103"),
    ("7.2.3", "twr-02", "198.18.106.102", "198.18.106.101"),
    ("7.2.4", "twr-02", "198.18.106.102", "198.18.106.103"),
    ("7.2.5", "twr-03", "198.18.106.103", "198.18.106.101"),
    ("7.2.6", "twr-03", "198.18.106.103", "198.18.106.102"),
]

# ============================================================================
# Section 9: Convergence & Resilience
# ============================================================================

# Wait times for convergence tests
ISIS_CONVERGENCE_WAIT = 20  # seconds for IS-IS SPF across 3 hops
BGP_HOLD_TIMER_WAIT = 25    # seconds (15s hold + margin)

# ============================================================================
# Section 10: Interop-Specific
# ============================================================================

KNOWN_LIMITATIONS = [
    ("10.3.1", "MikroTik supports only EVPN Type 3 (IMET) and ETREE leaf"),
    ("10.3.2", "MikroTik VTEPs do not support ECMP"),
    ("10.3.3", "MikroTik VTEPs do not support bond/bridge/VLAN as VTEP source"),
    ("10.3.4", "MikroTik VTEPs do not operate within VRFs"),
    ("10.3.5", "MikroTik VXLAN does not support IGMP snooping when offloaded"),
    ("10.3.6", "MikroTik bridged VXLAN not supported by MLAG"),
]
