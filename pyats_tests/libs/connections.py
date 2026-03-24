"""Netmiko connection manager for pyATS test framework."""

import os
import logging
from netmiko import ConnectHandler

logger = logging.getLogger(__name__)

BASE_DIR = "/tmp/stubarea51"
SSH_KEY = os.path.join(BASE_DIR, "sherpa_ssh_key")

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


class ConnectionManager:
    """Manages persistent netmiko connections to all lab devices."""

    def __init__(self):
        self._connections = {}

    def connect_all(self):
        for name, params in DEVICES.items():
            logger.info("Connecting to %s (%s)...", name, params["host"])
            self._connections[name] = ConnectHandler(**params)
            logger.info("Connected to %s", name)

    def disconnect_all(self):
        for name, conn in self._connections.items():
            try:
                conn.disconnect()
                logger.info("Disconnected from %s", name)
            except Exception:
                logger.warning("Error disconnecting from %s", name, exc_info=True)
        self._connections.clear()

    def cmd(self, device, command, read_timeout=30):
        return self._connections[device].send_command(command, read_timeout=read_timeout)

    def cmd_config(self, device, commands, read_timeout=30):
        """Send configuration commands (IOS-XE config mode)."""
        return self._connections[device].send_config_set(commands, read_timeout=read_timeout)

    def ping_ios(self, device, target, count=3):
        return self.cmd(device, f"ping {target} repeat {count}")

    def ping_mk(self, device, target, count=3, src=None):
        if src:
            return self.cmd(device, f"/ping {target} src-address={src} count={count}")
        return self.cmd(device, f"/ping {target} count={count}")

    def device_type(self, device):
        return DEVICES[device]["device_type"]

    def is_ios(self, device):
        return DEVICES[device]["device_type"] == "cisco_xe"

    def is_mk(self, device):
        return DEVICES[device]["device_type"] == "mikrotik_routeros"
