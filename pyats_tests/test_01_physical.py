"""Section 1: Physical / Link Layer tests."""

import logging
from pyats import aetest

from libs.connections import ConnectionManager
from libs.testdata import INTERFACE_STATE_CHECKS, MTU_CHECKS
from libs.parsers import interface_up_ios, interface_running_mk, get_mtu_ios, get_mtu_mk

logger = logging.getLogger(__name__)


class CommonSetup(aetest.CommonSetup):

    @aetest.subsection
    def connect_devices(self):
        conn_mgr = ConnectionManager()
        conn_mgr.connect_all()
        self.parent.parameters["conn_mgr"] = conn_mgr


class InterfaceState(aetest.Testcase):
    """1.1 — Interface state verification."""

    @aetest.setup
    def setup(self):
        self.conn = self.parent.parameters["conn_mgr"]

    @aetest.test
    @aetest.loop(check=INTERFACE_STATE_CHECKS)
    def test_interface_up(self, check):
        test_id, device, interface, dev_type = check
        logger.info("[%s] Checking %s %s is up", test_id, device, interface)

        if dev_type == "ios":
            output = self.conn.cmd(device, "show ip interface brief")
            assert interface_up_ios(output, interface), \
                f"{device} {interface} is not up/up:\n{output}"
        else:
            output = self.conn.cmd(device, f"/interface print where name={interface}")
            assert interface_running_mk(output, interface), \
                f"{device} {interface} is not running:\n{output}"


class MtuVerification(aetest.Testcase):
    """1.2 — MTU verification (>= 9000 for VXLAN overhead)."""

    @aetest.setup
    def setup(self):
        self.conn = self.parent.parameters["conn_mgr"]

    @aetest.test
    @aetest.loop(check=MTU_CHECKS)
    def test_mtu_jumbo(self, check):
        test_id, device, interfaces, dev_type = check
        logger.info("[%s] Checking %s MTU >= 9000 on %s", test_id, device, interfaces)

        if dev_type == "ios":
            output = self.conn.cmd(device, "show interfaces")
            for iface in interfaces:
                mtu = get_mtu_ios(output, iface)
                assert mtu >= 9000, f"{device} {iface} MTU is {mtu}, expected >= 9000"
        else:
            output = self.conn.cmd(device, "/interface ethernet print")
            mtus = get_mtu_mk(output)
            for iface in interfaces:
                mtu = mtus.get(iface, 0)
                assert mtu >= 9000, f"{device} {iface} MTU is {mtu}, expected >= 9000"


class CommonCleanup(aetest.CommonCleanup):

    @aetest.subsection
    def disconnect_devices(self):
        conn_mgr = self.parent.parameters.get("conn_mgr")
        if conn_mgr:
            conn_mgr.disconnect_all()


if __name__ == "__main__":
    aetest.main()
