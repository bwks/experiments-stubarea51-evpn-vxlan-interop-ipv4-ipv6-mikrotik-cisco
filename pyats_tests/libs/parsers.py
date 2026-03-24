"""Output parsing helpers for IOS-XE and MikroTik command output."""

import re


def ping_success_ios(output):
    """Check IOS-XE ping output for 100% success."""
    return "Success rate is 100 percent" in output


def ping_success_mk(output):
    """Check MikroTik ping output for 0% packet loss."""
    if "packet-loss=0%" in output:
        return True
    if "0% packet loss" in output:
        return True
    lines = output.strip().splitlines()
    for line in lines:
        if "timeout" in line.lower() and "HOST" not in line:
            return False
    m = re.search(r"sent=(\d+)\s+received=(\d+)", output)
    if m:
        return int(m.group(1)) == int(m.group(2)) and int(m.group(1)) > 0
    return False


def get_mtu_ios(output, interface):
    """Extract MTU value for a specific interface from IOS-XE output."""
    pattern = rf"{re.escape(interface)}.*?MTU\s+(\d+)"
    m = re.search(pattern, output, re.DOTALL)
    if m:
        return int(m.group(1))
    return 0


def get_mtu_mk(output):
    """Extract MTU values from MikroTik /interface ethernet print output.

    Handles both tabular format:
        #   NAME     MTU  MAC-ADDRESS        ARP
        0 R ether1  1500  52:54:00:FD:AA:B8  enabled
        1 R ether2  9000  52:54:00:DF:1F:D2  enabled

    And key=value detail format:
        name="ether2" mtu=9000
    """
    mtus = {}

    # Try tabular format first: "N R etherX  MMMM  ..."
    for line in output.splitlines():
        m = re.match(r'\s*\d+\s+\S*\s+(ether\d+)\s+(\d+)\s', line)
        if m:
            mtus[m.group(1)] = int(m.group(2))

    # Fall back to key=value format
    if not mtus:
        current_iface = None
        for line in output.splitlines():
            name_match = re.search(r'name="?(\S+)"?', line)
            if name_match:
                current_iface = name_match.group(1).strip('"')
            mtu_match = re.search(r'mtu=(\d+)', line)
            if mtu_match and current_iface:
                mtus[current_iface] = int(mtu_match.group(1))

    return mtus


def interface_up_ios(output, interface):
    """Check if IOS-XE interface is up/up."""
    for line in output.splitlines():
        if interface in line:
            parts = line.split()
            if len(parts) >= 6 and parts[-2].lower() == "up" and parts[-1].lower() == "up":
                return True
    return False


def interface_running_mk(output, interface):
    """Check if MikroTik interface is running."""
    for line in output.splitlines():
        if interface in line:
            if re.match(r'.*\bR\b.*' + re.escape(interface), line):
                return True
            if "running" in line.lower():
                return True
    return False


def has_substring(output, substring):
    """Simple substring check in output."""
    return substring in output


def has_substring_ci(output, substring):
    """Case-insensitive substring check."""
    return substring.lower() in output.lower()


def bgp_session_established_ios(output, neighbor_ip):
    """Check if BGP neighbor is established on IOS-XE.

    Handles case-insensitive matching for IPv6 addresses.
    IOS-XE wraps long IPv6 neighbors across two lines:
        3FFF:1AB:D127:D50::101
                    4   4208675309   ...   0
    """
    lines = output.splitlines()
    for i, line in enumerate(lines):
        if neighbor_ip.lower() in line.lower():
            # Check current line first (IPv4 — all on one line)
            parts = line.split()
            if parts:
                try:
                    int(parts[-1])
                    return True
                except ValueError:
                    pass
            # IPv6 wrap: data is on the next line
            if i + 1 < len(lines):
                next_parts = lines[i + 1].split()
                if next_parts:
                    try:
                        int(next_parts[-1])
                        return True
                    except ValueError:
                        pass
    return False


def bgp_session_established_mk(output, neighbor_ip):
    """Check if BGP session is established on MikroTik.

    MikroTik shows established sessions with 'E' flag:
        Flags: E - established
         0 E name="bgp-peer-ipv4-core-01-1" ...
             remote.address=100.127.1.1 ...
    """
    lines = output.splitlines()
    # Look for entries with 'E' flag that contain the neighbor IP
    in_entry = False
    entry_established = False
    for line in lines:
        # New entry starts with a number
        if re.match(r'\s*\d+\s', line):
            in_entry = True
            entry_established = " E " in line or line.strip().startswith("E ")
            if neighbor_ip in line and entry_established:
                return True
        elif in_entry:
            if neighbor_ip in line and entry_established:
                return True
            if line.strip() == "":
                in_entry = False
                entry_established = False

    return False


def isis_neighbor_present_ios(output, neighbor_name):
    """Check if IS-IS neighbor is present and up on IOS-XE.

    IOS-XE shows state as "UP" (uppercase).
    """
    for line in output.splitlines():
        if neighbor_name in line and "UP" in line.upper():
            return True
    return False


def isis_neighbor_present_mk(output, system_id):
    """Check if IS-IS neighbor is present on MikroTik."""
    return system_id in output
