"""Section 8: MAC Learning & Forwarding tests."""

import logging
from pyats import aetest

from libs.connections import ConnectionManager
from libs.parsers import has_substring, ping_success_mk

logger = logging.getLogger(__name__)


class CommonSetup(aetest.CommonSetup):

    @aetest.subsection
    def connect_devices(self):
        conn_mgr = ConnectionManager()
        conn_mgr.connect_all()
        self.parent.parameters["conn_mgr"] = conn_mgr

    @aetest.subsection
    def generate_traffic(self):
        """Ping between twr-01 and twr-02 to populate MAC tables."""
        conn = self.parent.parameters["conn_mgr"]
        conn.ping_mk("twr-01", "198.18.104.102", src="198.18.104.101")


class MACLearning(aetest.Testcase):
    """8.1 — Control-plane MAC learning."""

    @aetest.setup
    def setup(self):
        self.conn = self.parent.parameters["conn_mgr"]

    @aetest.test
    def test_twr01_bridge_hosts(self):
        """8.1.1 — After ping, twr-02 MAC visible on twr-01 bridge table."""
        output = self.conn.cmd("twr-01", "/interface bridge host print where bridge=br-router")
        # Should have entries from VXLAN interfaces
        assert "vxlan" in output.lower() or len(output.strip().splitlines()) > 1, \
            f"twr-01 bridge host table appears empty:\n{output}"

    @aetest.test
    def test_twr02_bridge_hosts(self):
        """8.1.2 — After ping, twr-01 MAC visible on twr-02 bridge table."""
        output = self.conn.cmd("twr-02", "/interface bridge host print where bridge=br-router")
        assert "vxlan" in output.lower() or len(output.strip().splitlines()) > 1, \
            f"twr-02 bridge host table appears empty:\n{output}"

    @aetest.test
    def test_learning_disabled(self):
        """8.1.3 — VXLAN interface shows learning=no."""
        for device in ["twr-01", "twr-02", "twr-03"]:
            output = self.conn.cmd(device, "/interface vxlan print detail")
            assert "dont-learn" in output.lower() or "learning=no" in output.lower(), \
                f"{device} VXLAN learning not disabled:\n{output}"


class CommonCleanup(aetest.CommonCleanup):

    @aetest.subsection
    def disconnect_devices(self):
        conn_mgr = self.parent.parameters.get("conn_mgr")
        if conn_mgr:
            conn_mgr.disconnect_all()


if __name__ == "__main__":
    aetest.main()
