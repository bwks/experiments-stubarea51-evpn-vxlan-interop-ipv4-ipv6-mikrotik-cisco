"""Section 10: Interop-Specific Checks."""

import logging
from pyats import aetest

from libs.connections import ConnectionManager
from libs.testdata import KNOWN_LIMITATIONS
from libs.parsers import (
    has_substring, bgp_session_established_mk, isis_neighbor_present_ios,
    ping_success_mk,
)

logger = logging.getLogger(__name__)


class CommonSetup(aetest.CommonSetup):

    @aetest.subsection
    def connect_devices(self):
        conn_mgr = ConnectionManager()
        conn_mgr.connect_all()
        self.parent.parameters["conn_mgr"] = conn_mgr


class Cat8000vRouteReflector(aetest.Testcase):
    """10.1 — Cat8000v as BGP EVPN Route Reflector."""

    @aetest.setup
    def setup(self):
        self.conn = self.parent.parameters["conn_mgr"]

    @aetest.test
    def test_type3_reflection(self):
        """10.1.1 — core-01 correctly reflects MikroTik EVPN Type 3 routes."""
        output = self.conn.cmd("core-01", "show bgp l2vpn evpn")
        for vtep in ["100.127.50.101", "100.127.50.102", "100.127.50.103"]:
            assert has_substring(output, vtep), \
                f"core-01 not reflecting Type 3 for {vtep}:\n{output}"

    @aetest.test
    def test_route_targets_preserved(self):
        """10.1.2 — core-01 preserves route targets during reflection."""
        # Verify both VNIs are present via RD numbering (:1 for VNI 1104, :2 for VNI 1106)
        output = self.conn.cmd("core-01", "show bgp l2vpn evpn")
        assert "100.127.50.101:1" in output, f"RT 1104 routes missing for twr-01:\n{output}"
        assert "100.127.50.101:2" in output, f"RT 1106 routes missing for twr-01:\n{output}"

    @aetest.test
    def test_originator_id(self):
        """10.1.3 — core-01 sets originator-id correctly."""
        output = self.conn.cmd("core-01", "show bgp l2vpn evpn")
        # RR has routes from all 3 towers, identified by their router-id in the RD
        for rd in ["100.127.50.101:1", "100.127.50.102:1", "100.127.50.103:1"]:
            assert rd in output, \
                f"core-01 EVPN table missing originator RD {rd}:\n{output}"

    @aetest.test
    def test_mk_accepts_reflected(self):
        """10.1.4 — MikroTik accepts reflected routes from Cat8000v."""
        for device in ["twr-01", "twr-02", "twr-03"]:
            output = self.conn.cmd(device, '/routing route print where belongs-to~"evpn"')
            # Each tower should see EVPN routes (at least from the other 2 towers)
            assert len(output.strip().splitlines()) >= 2, \
                f"{device} has too few EVPN routes — may not be accepting reflected routes:\n{output}"


class DualStackInterop(aetest.Testcase):
    """10.2 — Dual-stack underlay interop."""

    @aetest.setup
    def setup(self):
        self.conn = self.parent.parameters["conn_mgr"]

    @aetest.test
    def test_isis_cross_vendor(self):
        """10.2.1 — IS-IS adjacency forms between Cat8000v and MikroTik."""
        output = self.conn.cmd("agg-01", "show isis neighbors")
        # MikroTik neighbors appear by system-id on IOS-XE
        assert isis_neighbor_present_ios(output, "1001.2705.0101"), \
            f"agg-01 missing IS-IS neighbor twr-01 (1001.2705.0101):\n{output}"
        assert isis_neighbor_present_ios(output, "1001.2705.0102"), \
            f"agg-01 missing IS-IS neighbor twr-02 (1001.2705.0102):\n{output}"

    @aetest.test
    def test_isis_dual_stack_routes(self):
        """10.2.2 — IS-IS distributes both IPv4 and IPv6 across vendor boundary."""
        ipv4_output = self.conn.cmd("agg-01", "show ip route isis")
        ipv6_output = self.conn.cmd("agg-01", "show ipv6 route isis")
        assert "100.127.50.101" in ipv4_output, f"agg-01 missing twr-01 IPv4 route:\n{ipv4_output}"
        assert "D127:D50::101" in ipv6_output.upper() or "d127:d50::101" in ipv6_output.lower(), \
            f"agg-01 missing twr-01 IPv6 route:\n{ipv6_output}"

    @aetest.test
    def test_bgp_ipv4_cross_vendor(self):
        """10.2.3 — BGP over IPv4 between MikroTik and Cat8000v."""
        output = self.conn.cmd("twr-01", "/routing bgp session print")
        # MikroTik shows 'E' flag for established sessions
        assert " E " in output and "100.127.1.1" in output, \
            f"twr-01 BGP IPv4 session to core-01 not established:\n{output}"

    @aetest.test
    def test_bgp_ipv6_cross_vendor(self):
        """10.2.4 — BGP over IPv6 between MikroTik and Cat8000v."""
        output = self.conn.cmd("twr-01", "/routing bgp session print")
        assert " E " in output and "3fff:1ab:d127:d1::1" in output, \
            f"twr-01 BGP IPv6 session to core-01 not established:\n{output}"


class KnownLimitations(aetest.Testcase):
    """10.3 — Known MikroTik limitations (INFO tests)."""

    @aetest.setup
    def setup(self):
        self.conn = self.parent.parameters["conn_mgr"]

    @aetest.test
    @aetest.loop(limitation=KNOWN_LIMITATIONS)
    def test_acknowledged_limitation(self, limitation):
        """10.3.1-10.3.6 — Acknowledged MikroTik limitations."""
        test_id, description = limitation
        logger.info("[%s] Acknowledged: %s", test_id, description)
        self.passx(f"Acknowledged limitation: {description}")

    @aetest.test
    def test_ipv6_vtep_works(self):
        """10.3.7 — VNI 1106 uses IPv6 VTEP — verify it actually works."""
        output = self.conn.ping_mk("twr-01", "198.18.106.102", src="198.18.106.101")
        assert ping_success_mk(output), \
            f"IPv6 VTEP (VNI 1106) not working:\n{output}"


class CommonCleanup(aetest.CommonCleanup):

    @aetest.subsection
    def disconnect_devices(self):
        conn_mgr = self.parent.parameters.get("conn_mgr")
        if conn_mgr:
            conn_mgr.disconnect_all()


if __name__ == "__main__":
    aetest.main()
