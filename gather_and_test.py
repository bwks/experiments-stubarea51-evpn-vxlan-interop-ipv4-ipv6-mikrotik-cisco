#!/usr/bin/env python3
"""Gather running configs and execute test cases for EVPN/VXLAN interop lab."""

import os
import json
import time
from datetime import datetime, timezone
from netmiko import ConnectHandler

BASE_DIR = "/tmp/stubarea51"
CONFIG_DIR = os.path.join(BASE_DIR, "configs", "running")
TEST_DIR = os.path.join(BASE_DIR, "test-outputs")
SSH_KEY = os.path.join(BASE_DIR, "sherpa_ssh_key")

os.makedirs(CONFIG_DIR, exist_ok=True)
os.makedirs(TEST_DIR, exist_ok=True)

# Device definitions
DEVICES = {
    "core-01": {
        "device_type": "cisco_xe",
        "host": "172.31.1.11",
        "username": "sherpa",
        "use_keys": True,
        "key_file": SSH_KEY,
        "timeout": 30,
        "session_timeout": 60,
    },
    "agg-01": {
        "device_type": "cisco_xe",
        "host": "172.31.1.12",
        "username": "sherpa",
        "use_keys": True,
        "key_file": SSH_KEY,
        "timeout": 30,
        "session_timeout": 60,
    },
    "twr-01": {
        "device_type": "mikrotik_routeros",
        "host": "172.31.1.13",
        "username": "sherpa",
        "use_keys": True,
        "key_file": SSH_KEY,
        "timeout": 30,
        "session_timeout": 60,
    },
    "twr-02": {
        "device_type": "mikrotik_routeros",
        "host": "172.31.1.14",
        "username": "sherpa",
        "use_keys": True,
        "key_file": SSH_KEY,
        "timeout": 30,
        "session_timeout": 60,
    },
    "twr-03": {
        "device_type": "mikrotik_routeros",
        "host": "172.31.1.15",
        "username": "sherpa",
        "use_keys": True,
        "key_file": SSH_KEY,
        "timeout": 30,
        "session_timeout": 60,
    },
}


def connect(name):
    print(f"  Connecting to {name} ({DEVICES[name]['host']})...")
    conn = ConnectHandler(**DEVICES[name])
    return conn


def run_cmd(conn, cmd, device_type):
    if device_type == "cisco_xe":
        return conn.send_command(cmd, read_timeout=30)
    else:
        return conn.send_command(cmd, read_timeout=30)


def save(path, content):
    with open(path, "w") as f:
        f.write(content)


# ============================================================================
# Phase 1: Gather running configs
# ============================================================================
def gather_configs():
    print("\n=== Phase 1: Gathering running configs ===")
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    for name, params in DEVICES.items():
        conn = connect(name)
        if params["device_type"] == "cisco_xe":
            config = conn.send_command("show running-config", read_timeout=60)
            ext = "cfg"
        else:
            config = conn.send_command("/export", read_timeout=60)
            ext = "rsc"
        save(os.path.join(CONFIG_DIR, f"{name}.{ext}"), config + "\n")
        print(f"  Saved {name}.{ext}")
        conn.disconnect()

    # Write timestamp
    save(os.path.join(CONFIG_DIR, "collected_at.txt"), f"Configs collected at: {ts}\n")
    print(f"  Timestamp: {ts}")


# ============================================================================
# Phase 2: Run test cases
# ============================================================================
def run_tests():
    print("\n=== Phase 2: Running test cases ===")
    results = {}

    # Open persistent connections
    conns = {}
    for name in DEVICES:
        conns[name] = connect(name)

    def cmd(device, command):
        return run_cmd(conns[device], command, DEVICES[device]["device_type"])

    def mk_ping(device, target, count=3):
        return cmd(device, f"/ping {target} count={count}")

    def ios_ping(device, target, count=3):
        return cmd(device, f"ping {target} repeat {count}")

    # ------------------------------------------------------------------
    # Section 1: Physical / Link Layer
    # ------------------------------------------------------------------
    print("\n--- Section 1: Physical / Link Layer ---")

    results["1.1_interface_state"] = {}
    # IOS-XE
    for dev in ["core-01", "agg-01"]:
        out = cmd(dev, "show ip interface brief")
        results["1.1_interface_state"][dev] = out
        print(f"  1.1 {dev}: collected")

    # MikroTik
    for dev in ["twr-01", "twr-02", "twr-03"]:
        out = cmd(dev, "/interface print")
        results["1.1_interface_state"][dev] = out
        print(f"  1.1 {dev}: collected")

    results["1.2_mtu"] = {}
    for dev in ["core-01", "agg-01"]:
        out = cmd(dev, "show interfaces | include MTU|line protocol")
        results["1.2_mtu"][dev] = out
        print(f"  1.2 {dev}: collected")
    for dev in ["twr-01", "twr-02", "twr-03"]:
        out = cmd(dev, "/interface ethernet print")
        results["1.2_mtu"][dev] = out
        print(f"  1.2 {dev}: collected")

    # ------------------------------------------------------------------
    # Section 2: IP Addressing
    # ------------------------------------------------------------------
    print("\n--- Section 2: IP Addressing ---")

    results["2.1_ipv4_addressing"] = {}
    results["2.2_ipv6_addressing"] = {}
    results["2.3_loopback"] = {}

    for dev in ["core-01", "agg-01"]:
        results["2.1_ipv4_addressing"][dev] = cmd(dev, "show ip interface brief")
        results["2.2_ipv6_addressing"][dev] = cmd(dev, "show ipv6 interface brief")
        results["2.3_loopback"][dev] = cmd(dev, "show ip interface Loopback0")
        print(f"  2.1-2.3 {dev}: collected")

    for dev in ["twr-01", "twr-02", "twr-03"]:
        results["2.1_ipv4_addressing"][dev] = cmd(dev, "/ip address print")
        results["2.2_ipv6_addressing"][dev] = cmd(dev, "/ipv6 address print")
        results["2.3_loopback"][dev] = cmd(dev, "/ip address print where interface~\"lo\"")
        print(f"  2.1-2.3 {dev}: collected")

    # 2.4 Direct-link IPv4 pings
    print("  2.4 IPv4 link pings...")
    results["2.4_ipv4_link_pings"] = {}
    ping_tests_24 = [
        ("core-01", "100.126.1.50", "ios"),
        ("agg-01", "100.126.1.49", "ios"),
        ("agg-01", "100.126.50.2", "ios"),
        ("agg-01", "100.126.50.18", "ios"),
        ("twr-01", "100.126.50.10", "mk"),
        ("twr-02", "100.126.50.26", "mk"),
    ]
    for src, target, typ in ping_tests_24:
        key = f"{src}_to_{target}"
        if typ == "ios":
            results["2.4_ipv4_link_pings"][key] = ios_ping(src, target)
        else:
            results["2.4_ipv4_link_pings"][key] = mk_ping(src, target)
        print(f"    {src} → {target}: done")

    # 2.5 Direct-link IPv6 pings
    print("  2.5 IPv6 link pings...")
    results["2.5_ipv6_link_pings"] = {}
    ping_tests_25 = [
        ("core-01", "3fff:1ab:d1:d48::50", "ios"),
        ("agg-01", "3fff:1ab:d1:d48::49", "ios"),
        ("agg-01", "3fff:1ab:d50:d0::2", "ios"),
        ("agg-01", "3fff:1ab:d50:d16::d18", "ios"),
        ("twr-01", "3fff:1ab:d50:d8::10", "mk"),
        ("twr-02", "3fff:1ab:d50:d24::26", "mk"),
    ]
    for src, target, typ in ping_tests_25:
        key = f"{src}_to_{target}"
        if typ == "ios":
            results["2.5_ipv6_link_pings"][key] = ios_ping(src, target)
        else:
            results["2.5_ipv6_link_pings"][key] = mk_ping(src, target)
        print(f"    {src} → {target}: done")

    # ------------------------------------------------------------------
    # Section 3: IS-IS Underlay
    # ------------------------------------------------------------------
    print("\n--- Section 3: IS-IS Underlay ---")

    results["3.1_isis_neighbors"] = {}
    for dev in ["core-01", "agg-01"]:
        results["3.1_isis_neighbors"][dev] = cmd(dev, "show isis neighbors")
        print(f"  3.1 {dev}: collected")
    for dev in ["twr-01", "twr-02", "twr-03"]:
        results["3.1_isis_neighbors"][dev] = cmd(dev, "/routing isis neighbor print")
        print(f"  3.1 {dev}: collected")

    results["3.2_isis_instance"] = {}
    for dev in ["core-01", "agg-01"]:
        results["3.2_isis_instance"][dev] = cmd(dev, "show clns protocol")
        print(f"  3.2 {dev}: collected")
    for dev in ["twr-01", "twr-02", "twr-03"]:
        results["3.2_isis_instance"][dev] = cmd(dev, "/routing isis instance print")
        print(f"  3.2 {dev}: collected")

    results["3.3_isis_ipv4_routes"] = {}
    for dev in ["core-01", "agg-01"]:
        results["3.3_isis_ipv4_routes"][dev] = cmd(dev, "show ip route isis")
        print(f"  3.3 {dev}: collected")
    for dev in ["twr-01", "twr-02", "twr-03"]:
        results["3.3_isis_ipv4_routes"][dev] = cmd(dev, "/ip route print where routing-table=main and belongs-to~\"isis\"")
        print(f"  3.3 {dev}: collected")

    results["3.4_isis_ipv6_routes"] = {}
    for dev in ["core-01", "agg-01"]:
        results["3.4_isis_ipv6_routes"][dev] = cmd(dev, "show ipv6 route isis")
        print(f"  3.4 {dev}: collected")
    for dev in ["twr-01", "twr-02", "twr-03"]:
        results["3.4_isis_ipv6_routes"][dev] = cmd(dev, "/ipv6 route print where routing-table=main and belongs-to~\"isis\"")
        print(f"  3.4 {dev}: collected")

    # 3.5 Loopback-to-loopback IPv4 pings
    print("  3.5 Loopback IPv4 pings...")
    results["3.5_loopback_ipv4_pings"] = {}
    lo_pings_v4 = [
        ("twr-01", "100.127.1.1", "mk"),
        ("twr-02", "100.127.1.1", "mk"),
        ("twr-03", "100.127.1.1", "mk"),
        ("twr-01", "100.127.50.102", "mk"),
        ("twr-01", "100.127.50.103", "mk"),
        ("twr-02", "100.127.50.103", "mk"),
    ]
    for src, target, typ in lo_pings_v4:
        key = f"{src}_to_{target}"
        results["3.5_loopback_ipv4_pings"][key] = mk_ping(src, target)
        print(f"    {src} → {target}: done")

    # 3.6 Loopback-to-loopback IPv6 pings
    print("  3.6 Loopback IPv6 pings...")
    results["3.6_loopback_ipv6_pings"] = {}
    lo_pings_v6 = [
        ("twr-01", "3fff:1ab:d127:d1::1"),
        ("twr-02", "3fff:1ab:d127:d1::1"),
        ("twr-03", "3fff:1ab:d127:d1::1"),
        ("twr-01", "3fff:1ab:d127:d50::102"),
        ("twr-01", "3fff:1ab:d127:d50::103"),
        ("twr-02", "3fff:1ab:d127:d50::103"),
    ]
    for src, target in lo_pings_v6:
        key = f"{src}_to_{target}"
        results["3.6_loopback_ipv6_pings"][key] = mk_ping(src, target)
        print(f"    {src} → {target}: done")

    # ------------------------------------------------------------------
    # Section 4: BGP Control Plane
    # ------------------------------------------------------------------
    print("\n--- Section 4: BGP Control Plane ---")

    results["4.1_bgp_sessions"] = {}
    results["4.1_bgp_sessions"]["core-01_ipv4"] = cmd("core-01", "show bgp summary")
    results["4.1_bgp_sessions"]["core-01_ipv6"] = cmd("core-01", "show bgp ipv6 unicast summary")
    results["4.1_bgp_sessions"]["core-01_evpn"] = cmd("core-01", "show bgp l2vpn evpn summary")
    print("  4.1 core-01: collected")

    for dev in ["twr-01", "twr-02", "twr-03"]:
        results["4.1_bgp_sessions"][dev] = cmd(dev, "/routing bgp session print")
        print(f"  4.1 {dev}: collected")

    results["4.2_bgp_afi"] = {}
    results["4.2_bgp_afi"]["core-01"] = cmd("core-01", "show bgp neighbors | include neighbor|AFI")
    for dev in ["twr-01", "twr-02", "twr-03"]:
        results["4.2_bgp_afi"][dev] = cmd(dev, "/routing bgp connection print")
        print(f"  4.2 {dev}: collected")

    results["4.3_route_reflector"] = {}
    results["4.3_route_reflector"]["core-01_evpn_table"] = cmd("core-01", "show bgp l2vpn evpn")
    print("  4.3 core-01 EVPN table: collected")

    results["4.4_bgp_timers"] = {}
    results["4.4_bgp_timers"]["core-01"] = cmd("core-01", "show bgp neighbors | include timer|hold|keepalive")
    for dev in ["twr-01", "twr-02", "twr-03"]:
        results["4.4_bgp_timers"][dev] = cmd(dev, "/routing bgp template print")
    print("  4.4 BGP timers: collected")

    # ------------------------------------------------------------------
    # Section 5: EVPN Control Plane
    # ------------------------------------------------------------------
    print("\n--- Section 5: EVPN Control Plane ---")

    results["5.1_evpn_type3"] = {}
    results["5.1_evpn_type3"]["core-01"] = cmd("core-01", "show bgp l2vpn evpn")
    for dev in ["twr-01", "twr-02", "twr-03"]:
        results["5.1_evpn_type3"][dev] = cmd(dev, "/routing route print where belongs-to~\"evpn\"")
    print("  5.1 EVPN Type 3 routes: collected")

    results["5.2_evpn_reflection"] = {}
    for dev in ["twr-01", "twr-02", "twr-03"]:
        results["5.2_evpn_reflection"][dev] = cmd(dev, "/routing bgp session print")
    print("  5.2 EVPN reflection (prefix counts): collected")

    results["5.3_evpn_rt"] = {}
    for dev in ["twr-01", "twr-02", "twr-03"]:
        results["5.3_evpn_rt"][dev] = cmd(dev, "/routing bgp evpn print")
    print("  5.3 EVPN route targets: collected")

    results["5.4_evpn_counts"] = {}
    results["5.4_evpn_counts"]["core-01"] = cmd("core-01", "show bgp l2vpn evpn summary")
    print("  5.4 EVPN route counts: collected")

    # ------------------------------------------------------------------
    # Section 6: VXLAN Data Plane
    # ------------------------------------------------------------------
    print("\n--- Section 6: VXLAN Data Plane ---")

    results["6.1_vxlan_interfaces"] = {}
    for dev in ["twr-01", "twr-02", "twr-03"]:
        results["6.1_vxlan_interfaces"][dev] = cmd(dev, "/interface vxlan print detail")
    print("  6.1 VXLAN interfaces: collected")

    results["6.2_vtep_discovery"] = {}
    for dev in ["twr-01", "twr-02", "twr-03"]:
        results["6.2_vtep_discovery"][dev] = cmd(dev, "/interface vxlan vteps print")
    print("  6.2 VTEP discovery: collected")

    results["6.3_bridge_vlan"] = {}
    for dev in ["twr-01", "twr-02", "twr-03"]:
        results["6.3_bridge_vlan"][dev] = cmd(dev, "/interface bridge vlan print")
    print("  6.3 Bridge VLAN bindings: collected")

    # ------------------------------------------------------------------
    # Section 7: Overlay Connectivity
    # ------------------------------------------------------------------
    print("\n--- Section 7: Overlay Connectivity ---")

    # 7.1 VNI 1104
    results["7.1_vni1104_pings"] = {}
    vni1104_pings = [
        ("twr-01", "198.18.104.102"),
        ("twr-01", "198.18.104.103"),
        ("twr-02", "198.18.104.101"),
        ("twr-02", "198.18.104.103"),
        ("twr-03", "198.18.104.101"),
        ("twr-03", "198.18.104.102"),
    ]
    for src, target in vni1104_pings:
        key = f"{src}_to_{target}"
        results["7.1_vni1104_pings"][key] = mk_ping(src, target)
        print(f"  7.1 {src} → {target}: done")

    # 7.2 VNI 1106
    results["7.2_vni1106_pings"] = {}
    vni1106_pings = [
        ("twr-01", "198.18.106.102"),
        ("twr-01", "198.18.106.103"),
        ("twr-02", "198.18.106.101"),
        ("twr-02", "198.18.106.103"),
        ("twr-03", "198.18.106.101"),
        ("twr-03", "198.18.106.102"),
    ]
    for src, target in vni1106_pings:
        key = f"{src}_to_{target}"
        results["7.2_vni1106_pings"][key] = mk_ping(src, target)
        print(f"  7.2 {src} → {target}: done")

    # 7.3 Cross-VNI (INFO tests)
    results["7.3_cross_vni"] = {}
    results["7.3_cross_vni"]["twr-01_1104_to_1106_local"] = mk_ping("twr-01", "198.18.106.101")
    results["7.3_cross_vni"]["twr-01_1104_to_twr-02_1106"] = mk_ping("twr-01", "198.18.106.102")
    print("  7.3 Cross-VNI: done")

    # ------------------------------------------------------------------
    # Section 8: MAC Learning
    # ------------------------------------------------------------------
    print("\n--- Section 8: MAC Learning ---")

    results["8.1_mac_learning"] = {}
    for dev in ["twr-01", "twr-02", "twr-03"]:
        results["8.1_mac_learning"][dev + "_bridge_hosts"] = cmd(dev, "/interface bridge host print where bridge=br-router")
        results["8.1_mac_learning"][dev + "_vxlan_detail"] = cmd(dev, "/interface vxlan print detail")
    print("  8.1 MAC learning: collected")

    # ------------------------------------------------------------------
    # Section 9: SKIPPED (shutdown/reload tests)
    # ------------------------------------------------------------------
    print("\n--- Section 9: SKIPPED (shutdown/reload tests) ---")
    results["9_skipped"] = "Section 9 (Convergence & Resilience) skipped — tests involve shutting down interfaces/devices."

    # ------------------------------------------------------------------
    # Section 10: Interop-Specific
    # ------------------------------------------------------------------
    print("\n--- Section 10: Interop-Specific ---")

    results["10.1_route_reflector"] = {}
    results["10.1_route_reflector"]["core-01_evpn_detail"] = cmd("core-01", "show bgp l2vpn evpn")
    for dev in ["twr-01", "twr-02", "twr-03"]:
        results["10.1_route_reflector"][dev + "_sessions"] = cmd(dev, "/routing bgp session print")
        results["10.1_route_reflector"][dev + "_evpn_routes"] = cmd(dev, "/routing route print where belongs-to~\"evpn\"")
    print("  10.1 Route reflector checks: collected")

    results["10.2_dual_stack"] = {}
    for dev in ["core-01", "agg-01"]:
        results["10.2_dual_stack"][dev + "_isis_neighbors"] = cmd(dev, "show isis neighbors")
    for dev in ["twr-01", "twr-02", "twr-03"]:
        results["10.2_dual_stack"][dev + "_isis_neighbors"] = cmd(dev, "/routing isis neighbor print")
        results["10.2_dual_stack"][dev + "_bgp_sessions"] = cmd(dev, "/routing bgp session print")
    print("  10.2 Dual-stack interop: collected")

    results["10.3_limitations"] = {}
    for dev in ["twr-01", "twr-02", "twr-03"]:
        results["10.3_limitations"][dev + "_vxlan"] = cmd(dev, "/interface vxlan print detail")
        results["10.3_limitations"][dev + "_evpn"] = cmd(dev, "/routing bgp evpn print")
    print("  10.3 Known limitations data: collected")

    # Close connections
    for name, conn in conns.items():
        conn.disconnect()

    # Save results
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    save(os.path.join(TEST_DIR, "collected_at.txt"), f"Tests executed at: {ts}\n")

    for section_name, data in results.items():
        section_dir = os.path.join(TEST_DIR, section_name)
        os.makedirs(section_dir, exist_ok=True)
        if isinstance(data, str):
            save(os.path.join(section_dir, "note.txt"), data + "\n")
        elif isinstance(data, dict):
            for key, output in data.items():
                safe_key = key.replace("::", "_").replace("/", "_")
                save(os.path.join(section_dir, f"{safe_key}.txt"), output + "\n")

    print(f"\n  All test outputs saved to {TEST_DIR}/")
    print(f"  Timestamp: {ts}")


if __name__ == "__main__":
    start = time.time()
    gather_configs()
    run_tests()
    elapsed = time.time() - start
    print(f"\nComplete in {elapsed:.1f}s")
