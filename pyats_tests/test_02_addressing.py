"""Section 2: IP Addressing tests."""

import logging
from pyats import aetest

from libs.connections import ConnectionManager
from libs.testdata import (
    IPV4_LINK_ADDRESSES, IPV6_LINK_ADDRESSES, LOOPBACK_ADDRESSES,
    PING_TESTS_IPV4_LINK, PING_TESTS_IPV6_LINK,
)
from libs.parsers import has_substring, ping_success_ios, ping_success_mk

logger = logging.getLogger(__name__)


class CommonSetup(aetest.CommonSetup):

    @aetest.subsection
    def connect_devices(self):
        conn_mgr = ConnectionManager()
        conn_mgr.connect_all()
        self.parent.parameters["conn_mgr"] = conn_mgr


class IPv4LinkAddressing(aetest.Testcase):
    """2.1 — IPv4 point-to-point link addressing."""

    @aetest.setup
    def setup(self):
        self.conn = self.parent.parameters["conn_mgr"]
        # Cache output per device to avoid repeated commands
        self._cache = {}

    def _get_output(self, device, dev_type):
        if device not in self._cache:
            if dev_type == "ios":
                self._cache[device] = self.conn.cmd(device, "show ip interface brief")
            else:
                self._cache[device] = self.conn.cmd(device, "/ip address print")
        return self._cache[device]

    @aetest.test
    @aetest.loop(check=IPV4_LINK_ADDRESSES)
    def test_ipv4_address(self, check):
        test_id, device, interface, expected_addr, dev_type = check
        logger.info("[%s] Checking %s %s has %s", test_id, device, interface, expected_addr)
        output = self._get_output(device, dev_type)
        assert has_substring(output, expected_addr), \
            f"{device} missing {expected_addr}:\n{output}"


class IPv6LinkAddressing(aetest.Testcase):
    """2.2 — IPv6 point-to-point link addressing."""

    @aetest.setup
    def setup(self):
        self.conn = self.parent.parameters["conn_mgr"]
        self._cache = {}

    def _get_output(self, device, dev_type):
        if device not in self._cache:
            if dev_type == "ios":
                self._cache[device] = self.conn.cmd(device, "show ipv6 interface brief")
            else:
                self._cache[device] = self.conn.cmd(device, "/ipv6 address print")
        return self._cache[device]

    @aetest.test
    @aetest.loop(check=IPV6_LINK_ADDRESSES)
    def test_ipv6_address(self, check):
        test_id, device, interface, expected_addr, dev_type = check
        logger.info("[%s] Checking %s %s has %s", test_id, device, interface, expected_addr)
        output = self._get_output(device, dev_type)
        # IPv6 addresses are case-insensitive
        assert expected_addr.lower() in output.lower(), \
            f"{device} missing {expected_addr}:\n{output}"


class LoopbackAddressing(aetest.Testcase):
    """2.3 — Loopback addressing (IPv4 + IPv6)."""

    @aetest.setup
    def setup(self):
        self.conn = self.parent.parameters["conn_mgr"]

    @aetest.test
    @aetest.loop(check=LOOPBACK_ADDRESSES)
    def test_loopback(self, check):
        test_id, device, ipv4, ipv6, dev_type = check
        logger.info("[%s] Checking %s loopbacks: %s / %s", test_id, device, ipv4, ipv6)

        if dev_type == "ios":
            out_v4 = self.conn.cmd(device, "show ip interface Loopback0")
            out_v6 = self.conn.cmd(device, "show ipv6 interface Loopback0")
        else:
            out_v4 = self.conn.cmd(device, '/ip address print where interface~"lo"')
            out_v6 = self.conn.cmd(device, '/ipv6 address print where interface~"lo"')

        assert has_substring(out_v4, ipv4), f"{device} missing IPv4 loopback {ipv4}:\n{out_v4}"
        assert ipv6.lower() in out_v6.lower(), f"{device} missing IPv6 loopback {ipv6}:\n{out_v6}"


class IPv4LinkPings(aetest.Testcase):
    """2.4 — Direct-link IPv4 ping tests."""

    @aetest.setup
    def setup(self):
        self.conn = self.parent.parameters["conn_mgr"]

    @aetest.test
    @aetest.loop(check=PING_TESTS_IPV4_LINK)
    def test_ping(self, check):
        test_id, src, target, dev_type = check
        logger.info("[%s] Ping %s → %s", test_id, src, target)

        if dev_type == "ios":
            output = self.conn.ping_ios(src, target)
            assert ping_success_ios(output), f"Ping failed {src} → {target}:\n{output}"
        else:
            output = self.conn.ping_mk(src, target)
            assert ping_success_mk(output), f"Ping failed {src} → {target}:\n{output}"


class IPv6LinkPings(aetest.Testcase):
    """2.5 — Direct-link IPv6 ping tests."""

    @aetest.setup
    def setup(self):
        self.conn = self.parent.parameters["conn_mgr"]

    @aetest.test
    @aetest.loop(check=PING_TESTS_IPV6_LINK)
    def test_ping(self, check):
        test_id, src, target, dev_type = check
        logger.info("[%s] Ping %s → %s", test_id, src, target)

        if dev_type == "ios":
            output = self.conn.ping_ios(src, target)
            assert ping_success_ios(output), f"Ping failed {src} → {target}:\n{output}"
        else:
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
