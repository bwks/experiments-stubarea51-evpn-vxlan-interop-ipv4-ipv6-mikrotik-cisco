"""Section 3: IS-IS Underlay tests."""

import logging
from pyats import aetest

from libs.connections import ConnectionManager
from libs.testdata import (
    ISIS_NEIGHBORS, ISIS_INSTANCE_PARAMS, ISIS_IPV4_ROUTES, ISIS_IPV6_ROUTES,
    PING_TESTS_LOOPBACK_IPV4, PING_TESTS_LOOPBACK_IPV6,
)
from libs.parsers import (
    has_substring, isis_neighbor_present_ios, isis_neighbor_present_mk,
    ping_success_mk,
)

logger = logging.getLogger(__name__)


class CommonSetup(aetest.CommonSetup):

    @aetest.subsection
    def connect_devices(self):
        conn_mgr = ConnectionManager()
        conn_mgr.connect_all()
        self.parent.parameters["conn_mgr"] = conn_mgr


class ISISAdjacency(aetest.Testcase):
    """3.1 — IS-IS adjacency verification."""

    @aetest.setup
    def setup(self):
        self.conn = self.parent.parameters["conn_mgr"]
        self._cache = {}

    def _get_output(self, device, dev_type):
        if device not in self._cache:
            if dev_type == "ios":
                self._cache[device] = self.conn.cmd(device, "show isis neighbors")
            else:
                self._cache[device] = self.conn.cmd(device, "/routing isis neighbor print")
        return self._cache[device]

    @aetest.test
    @aetest.loop(check=ISIS_NEIGHBORS)
    def test_isis_neighbor(self, check):
        test_id, device, neighbor, interface, dev_type = check
        logger.info("[%s] Checking %s has IS-IS neighbor %s on %s", test_id, device, neighbor, interface)
        output = self._get_output(device, dev_type)

        if dev_type == "ios":
            assert isis_neighbor_present_ios(output, neighbor), \
                f"{device} missing IS-IS neighbor {neighbor}:\n{output}"
        else:
            assert isis_neighbor_present_mk(output, neighbor), \
                f"{device} missing IS-IS neighbor {neighbor}:\n{output}"


class ISISInstanceParams(aetest.Testcase):
    """3.2 — IS-IS instance parameters."""

    @aetest.setup
    def setup(self):
        self.conn = self.parent.parameters["conn_mgr"]

    @aetest.test
    @aetest.loop(check=ISIS_INSTANCE_PARAMS)
    def test_isis_param(self, check):
        test_id, device, param, expected, dev_type = check
        logger.info("[%s] Checking %s %s = %s", test_id, device, param, expected)

        if dev_type == "ios":
            output = self.conn.cmd(device, "show clns protocol")
        else:
            output = self.conn.cmd(device, "/routing isis instance print")

        assert has_substring(output, expected), \
            f"{device} missing {param}={expected}:\n{output}"


class ISISIPv4Routes(aetest.Testcase):
    """3.3 — IS-IS IPv4 route propagation."""

    @aetest.setup
    def setup(self):
        self.conn = self.parent.parameters["conn_mgr"]
        self._cache = {}

    def _get_output(self, device, dev_type):
        if device not in self._cache:
            if dev_type == "ios":
                self._cache[device] = self.conn.cmd(device, "show ip route isis")
            else:
                # RouterOS 7.20+ may not match belongs-to~"isis", use full route table
                self._cache[device] = self.conn.cmd(device, "/ip route print")
        return self._cache[device]

    @aetest.test
    @aetest.loop(check=ISIS_IPV4_ROUTES)
    def test_route(self, check):
        test_id, device, prefix, dev_type = check
        logger.info("[%s] Checking %s has IS-IS route for %s", test_id, device, prefix)
        output = self._get_output(device, dev_type)
        assert has_substring(output, prefix), \
            f"{device} missing route for {prefix}:\n{output}"


class ISISIPv6Routes(aetest.Testcase):
    """3.4 — IS-IS IPv6 route propagation."""

    @aetest.setup
    def setup(self):
        self.conn = self.parent.parameters["conn_mgr"]
        self._cache = {}

    def _get_output(self, device, dev_type):
        if device not in self._cache:
            if dev_type == "ios":
                self._cache[device] = self.conn.cmd(device, "show ipv6 route isis")
            else:
                self._cache[device] = self.conn.cmd(device, "/ipv6 route print")
        return self._cache[device]

    @aetest.test
    @aetest.loop(check=ISIS_IPV6_ROUTES)
    def test_route(self, check):
        test_id, device, prefix, dev_type = check
        logger.info("[%s] Checking %s has IS-IS IPv6 route for %s", test_id, device, prefix)
        output = self._get_output(device, dev_type)
        assert prefix.lower() in output.lower(), \
            f"{device} missing IPv6 route for {prefix}:\n{output}"


class LoopbackIPv4Pings(aetest.Testcase):
    """3.5 — Loopback-to-loopback reachability (IPv4)."""

    @aetest.setup
    def setup(self):
        self.conn = self.parent.parameters["conn_mgr"]

    @aetest.test
    @aetest.loop(check=PING_TESTS_LOOPBACK_IPV4)
    def test_ping(self, check):
        test_id, src, target = check
        logger.info("[%s] Ping %s → %s", test_id, src, target)
        output = self.conn.ping_mk(src, target)
        assert ping_success_mk(output), f"Ping failed {src} → {target}:\n{output}"


class LoopbackIPv6Pings(aetest.Testcase):
    """3.6 — Loopback-to-loopback reachability (IPv6)."""

    @aetest.setup
    def setup(self):
        self.conn = self.parent.parameters["conn_mgr"]

    @aetest.test
    @aetest.loop(check=PING_TESTS_LOOPBACK_IPV6)
    def test_ping(self, check):
        test_id, src, target = check
        logger.info("[%s] Ping %s → %s", test_id, src, target)
        output = self.conn.ping_mk(src, target)
        assert ping_success_mk(output), f"Ping failed {src} → {target}:\n{output}"


class CommonCleanup(aetest.CommonCleanup):

    @aetest.subsection
    def disconnect_devices(self):
        conn_mgr = self.parent.parameters.get("conn_mgr")
        if conn_mgr:
            conn_mgr.disconnect_all()


if __name__ == "__main__":
    aetest.main()
