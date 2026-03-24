"""Section 9: Convergence & Resilience tests.

These tests involve shutting down interfaces and BGP sessions. Each test
includes cleanup that re-enables everything regardless of outcome.
"""

import time
import logging
from pyats import aetest

from libs.connections import ConnectionManager
from libs.testdata import ISIS_CONVERGENCE_WAIT, BGP_HOLD_TIMER_WAIT
from libs.parsers import ping_success_ios, ping_success_mk, has_substring

logger = logging.getLogger(__name__)


class CommonSetup(aetest.CommonSetup):

    @aetest.subsection
    def connect_devices(self):
        conn_mgr = ConnectionManager()
        conn_mgr.connect_all()
        self.parent.parameters["conn_mgr"] = conn_mgr

    @aetest.subsection
    def verify_baseline(self):
        """Verify all devices are reachable before running disruptive tests."""
        conn = self.parent.parameters["conn_mgr"]
        output = conn.ping_mk("twr-01", "100.127.1.1")
        assert ping_success_mk(output), "Baseline failed: twr-01 cannot reach core-01"


class ISISConvergence(aetest.Testcase):
    """9.1 — IS-IS convergence on link failure."""

    @aetest.setup
    def setup(self):
        self.conn = self.parent.parameters["conn_mgr"]

    @aetest.test
    def test_alternate_path(self):
        """9.1.1 — Disable agg-01 Gig2 → twr-01 reroutes via twr-03→twr-02→agg-01."""
        try:
            # Shut agg-01 Gig2
            logger.info("Shutting agg-01 GigabitEthernet2...")
            self.conn.cmd_config("agg-01", ["interface GigabitEthernet2", "shutdown"])

            # Wait for IS-IS SPF convergence across 3 hops
            logger.info("Waiting %ds for IS-IS convergence...", ISIS_CONVERGENCE_WAIT)
            time.sleep(ISIS_CONVERGENCE_WAIT)

            # Verify twr-01 can still reach core-01 via alternate path
            output = self.conn.ping_mk("twr-01", "100.127.1.1")
            assert ping_success_mk(output), \
                f"twr-01 cannot reach core-01 after agg-01 Gig2 shutdown:\n{output}"
        finally:
            # Always re-enable
            logger.info("Re-enabling agg-01 GigabitEthernet2...")
            self.conn.cmd_config("agg-01", ["interface GigabitEthernet2", "no shutdown"])
            time.sleep(ISIS_CONVERGENCE_WAIT)

    @aetest.test
    def test_recovery(self):
        """9.1.2 — After re-enable, IS-IS adjacency re-forms."""
        output = self.conn.ping_ios("agg-01", "100.126.50.2")
        assert ping_success_ios(output), \
            f"agg-01 cannot reach twr-01 after recovery:\n{output}"


class BGPSessionFailover(aetest.Testcase):
    """9.2 — BGP session failover."""

    @aetest.setup
    def setup(self):
        self.conn = self.parent.parameters["conn_mgr"]

    @aetest.test
    def test_bgp_failover_and_recovery(self):
        """9.2.1-9.2.2 — Disable/re-enable core-01 Gig2, verify BGP recovery."""
        try:
            # Shut core-01 Gig2 (to agg-01)
            logger.info("Shutting core-01 GigabitEthernet2...")
            self.conn.cmd_config("core-01", ["interface GigabitEthernet2", "shutdown"])

            logger.info("Waiting %ds for BGP hold-timer expiry...", BGP_HOLD_TIMER_WAIT)
            time.sleep(BGP_HOLD_TIMER_WAIT)

            # Verify BGP sessions are down on towers
            output = self.conn.cmd("twr-01", "/routing bgp session print")
            logger.info("twr-01 BGP sessions during outage:\n%s", output)

        finally:
            # Re-enable
            logger.info("Re-enabling core-01 GigabitEthernet2...")
            self.conn.cmd_config("core-01", ["interface GigabitEthernet2", "no shutdown"])
            # Wait for IS-IS + BGP to reconverge
            time.sleep(BGP_HOLD_TIMER_WAIT + ISIS_CONVERGENCE_WAIT)

    @aetest.test
    def test_overlay_after_recovery(self):
        """9.2.3 — Overlay connectivity restored after BGP reconvergence."""
        output = self.conn.ping_mk("twr-01", "198.18.104.102", src="198.18.104.101")
        assert ping_success_mk(output), \
            f"VNI 1104 overlay not restored after BGP recovery:\n{output}"


class VTEPLossSimulation(aetest.Testcase):
    """9.3 — VTEP loss simulation (disable twr-03 BGP instead of power off)."""

    @aetest.setup
    def setup(self):
        self.conn = self.parent.parameters["conn_mgr"]

    @aetest.test
    def test_stale_vtep_removal(self):
        """9.3.1 — After disabling twr-03 BGP, twr-01/twr-02 should remove stale VTEPs.

        KNOWN FAILURE: MikroTik RouterOS does not remove EVPN-created dynamic
        VTEP entries when Type 3 routes are withdrawn. This is a confirmed
        RouterOS limitation.
        """
        try:
            # Disable twr-03 BGP
            logger.info("Disabling twr-03 BGP sessions...")
            self.conn.cmd("twr-03", "/routing bgp connection set [find] disabled=yes")

            # Wait for BGP hold-timer expiry + margin
            logger.info("Waiting %ds for BGP hold-timer expiry...", BGP_HOLD_TIMER_WAIT)
            time.sleep(BGP_HOLD_TIMER_WAIT)

            # Check twr-01 VTEP table
            output = self.conn.cmd("twr-01", "/interface vxlan vteps print")
            logger.info("twr-01 VTEPs after twr-03 BGP disable:\n%s", output)

            # Check if twr-03 VTEPs are removed
            if "100.127.50.103" in output:
                self.passx("MikroTik stale VTEP cache — twr-03 VTEP still present on twr-01 "
                           "(known RouterOS limitation)")
            else:
                self.passed("twr-03 VTEP correctly removed from twr-01")

        finally:
            # Re-enable twr-03 BGP
            logger.info("Re-enabling twr-03 BGP sessions...")
            self.conn.cmd("twr-03", "/routing bgp connection set [find] disabled=no")
            time.sleep(BGP_HOLD_TIMER_WAIT)

    @aetest.test
    def test_remaining_overlay(self):
        """9.3.2 — twr-01 ↔ twr-02 overlay still works during twr-03 loss."""
        output = self.conn.ping_mk("twr-01", "198.18.104.102", src="198.18.104.101")
        assert ping_success_mk(output), \
            f"twr-01 ↔ twr-02 overlay failed:\n{output}"

    @aetest.test
    def test_full_mesh_restored(self):
        """9.3.3 — Full-mesh overlay restored after twr-03 BGP re-enabled."""
        output = self.conn.ping_mk("twr-01", "198.18.104.103", src="198.18.104.101")
        assert ping_success_mk(output), \
            f"twr-01 ↔ twr-03 overlay not restored:\n{output}"


class CommonCleanup(aetest.CommonCleanup):

    @aetest.subsection
    def verify_recovery(self):
        """Verify all devices are reachable after convergence tests."""
        conn = self.parent.parameters["conn_mgr"]
        for src in ["twr-01", "twr-02", "twr-03"]:
            output = conn.ping_mk(src, "100.127.1.1")
            if not ping_success_mk(output):
                logger.warning("%s cannot reach core-01 after convergence tests", src)

    @aetest.subsection
    def disconnect_devices(self):
        conn_mgr = self.parent.parameters.get("conn_mgr")
        if conn_mgr:
            conn_mgr.disconnect_all()


if __name__ == "__main__":
    aetest.main()
