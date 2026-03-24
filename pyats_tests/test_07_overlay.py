"""Section 7: Overlay Connectivity tests."""

import logging
from pyats import aetest

from libs.connections import ConnectionManager
from libs.testdata import PING_TESTS_VNI1104, PING_TESTS_VNI1106
from libs.parsers import ping_success_mk

logger = logging.getLogger(__name__)


class CommonSetup(aetest.CommonSetup):

    @aetest.subsection
    def connect_devices(self):
        conn_mgr = ConnectionManager()
        conn_mgr.connect_all()
        self.parent.parameters["conn_mgr"] = conn_mgr


class VNI1104Connectivity(aetest.Testcase):
    """7.1 — VNI 1104 (IPv4 over IPv4 VXLAN) connectivity."""

    @aetest.setup
    def setup(self):
        self.conn = self.parent.parameters["conn_mgr"]

    @aetest.test
    @aetest.loop(check=PING_TESTS_VNI1104)
    def test_ping(self, check):
        test_id, src, src_ip, target_ip = check
        logger.info("[%s] Ping %s (%s) → %s", test_id, src, src_ip, target_ip)
        output = self.conn.ping_mk(src, target_ip, src=src_ip)
        assert ping_success_mk(output), \
            f"VNI 1104 ping failed {src} {src_ip} → {target_ip}:\n{output}"


class VNI1106Connectivity(aetest.Testcase):
    """7.2 — VNI 1106 (IPv4 over IPv6 VXLAN) connectivity."""

    @aetest.setup
    def setup(self):
        self.conn = self.parent.parameters["conn_mgr"]

    @aetest.test
    @aetest.loop(check=PING_TESTS_VNI1106)
    def test_ping(self, check):
        test_id, src, src_ip, target_ip = check
        logger.info("[%s] Ping %s (%s) → %s", test_id, src, src_ip, target_ip)
        output = self.conn.ping_mk(src, target_ip, src=src_ip)
        assert ping_success_mk(output), \
            f"VNI 1106 ping failed {src} {src_ip} → {target_ip}:\n{output}"


class OverlayIsolation(aetest.Testcase):
    """7.3 — Overlay isolation verification (INFO — cross-VNI routing is expected)."""

    @aetest.setup
    def setup(self):
        self.conn = self.parent.parameters["conn_mgr"]

    @aetest.test
    def test_cross_vni_local(self):
        """7.3.1 — Cross-VNI on same device (expected to succeed — INFO)."""
        output = self.conn.ping_mk("twr-01", "198.18.106.101")
        # This succeeds because both VNIs are L3 interfaces in the global table.
        # Reclassified as INFO — not a failure.
        if ping_success_mk(output):
            self.passx("Cross-VNI routing expected in this topology — "
                       "both VNIs are L3 interfaces in the global routing table")
        else:
            self.failed("Unexpected: cross-VNI ping failed, but both interfaces are in global table")

    @aetest.test
    def test_cross_vni_remote(self):
        """7.3.2 — Cross-VNI across devices (expected to succeed — INFO)."""
        output = self.conn.ping_mk("twr-01", "198.18.106.102")
        if ping_success_mk(output):
            self.passx("Cross-VNI routing expected in this topology — "
                       "routers have IP interfaces in both VNIs")
        else:
            self.failed("Unexpected: cross-VNI ping failed, but both interfaces are in global table")


class CommonCleanup(aetest.CommonCleanup):

    @aetest.subsection
    def disconnect_devices(self):
        conn_mgr = self.parent.parameters.get("conn_mgr")
        if conn_mgr:
            conn_mgr.disconnect_all()


if __name__ == "__main__":
    aetest.main()
