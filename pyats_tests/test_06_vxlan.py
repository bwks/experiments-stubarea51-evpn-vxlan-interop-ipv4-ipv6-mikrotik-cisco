"""Section 6: VXLAN Data Plane tests."""

import logging
from pyats import aetest

from libs.connections import ConnectionManager
from libs.testdata import VXLAN_INTERFACES, VTEP_DISCOVERY, BRIDGE_VLAN_BINDINGS
from libs.parsers import has_substring

logger = logging.getLogger(__name__)


class CommonSetup(aetest.CommonSetup):

    @aetest.subsection
    def connect_devices(self):
        conn_mgr = ConnectionManager()
        conn_mgr.connect_all()
        self.parent.parameters["conn_mgr"] = conn_mgr


class VXLANInterfaceVerification(aetest.Testcase):
    """6.1 — VXLAN interface verification."""

    @aetest.setup
    def setup(self):
        self.conn = self.parent.parameters["conn_mgr"]
        self._cache = {}

    def _get_output(self, device):
        if device not in self._cache:
            self._cache[device] = self.conn.cmd(device, "/interface vxlan print detail")
        return self._cache[device]

    @aetest.test
    @aetest.loop(check=VXLAN_INTERFACES)
    def test_vxlan_interface(self, check):
        test_id, device, vni, local_addr, learning = check
        logger.info("[%s] Checking %s VXLAN VNI %d, local=%s", test_id, device, vni, local_addr)
        output = self._get_output(device)
        assert has_substring(output, str(vni)), \
            f"{device} missing VNI {vni}:\n{output}"
        assert local_addr.lower() in output.lower(), \
            f"{device} missing local-address {local_addr}:\n{output}"
        # Check learning is disabled (dont-learn or learning=no)
        assert "dont-learn" in output.lower() or "learning=no" in output.lower(), \
            f"{device} VXLAN learning not disabled:\n{output}"


class DynamicVTEPDiscovery(aetest.Testcase):
    """6.2 — Dynamic VTEP discovery via EVPN."""

    @aetest.setup
    def setup(self):
        self.conn = self.parent.parameters["conn_mgr"]
        self._cache = {}

    def _get_output(self, device):
        if device not in self._cache:
            self._cache[device] = self.conn.cmd(device, "/interface vxlan vteps print")
        return self._cache[device]

    @aetest.test
    @aetest.loop(check=VTEP_DISCOVERY)
    def test_vtep_present(self, check):
        test_id, device, vni, expected_vteps = check
        logger.info("[%s] Checking %s VNI %d has VTEPs: %s", test_id, device, vni, expected_vteps)
        output = self._get_output(device)
        for vtep in expected_vteps:
            assert vtep.lower() in output.lower(), \
                f"{device} VNI {vni} missing VTEP {vtep}:\n{output}"


class BridgeVLANBinding(aetest.Testcase):
    """6.3 — VLAN-to-VNI bridge binding."""

    @aetest.setup
    def setup(self):
        self.conn = self.parent.parameters["conn_mgr"]
        self._cache = {}

    def _get_output(self, device):
        if device not in self._cache:
            self._cache[device] = self.conn.cmd(device, "/interface bridge vlan print")
        return self._cache[device]

    @aetest.test
    @aetest.loop(check=BRIDGE_VLAN_BINDINGS)
    def test_bridge_binding(self, check):
        test_id, device, vxlan_iface, pvid = check
        logger.info("[%s] Checking %s %s bound to VLAN %s", test_id, device, vxlan_iface, pvid)
        output = self._get_output(device)
        assert has_substring(output, pvid), \
            f"{device} missing VLAN {pvid} in bridge:\n{output}"


class CommonCleanup(aetest.CommonCleanup):

    @aetest.subsection
    def disconnect_devices(self):
        conn_mgr = self.parent.parameters.get("conn_mgr")
        if conn_mgr:
            conn_mgr.disconnect_all()


if __name__ == "__main__":
    aetest.main()
