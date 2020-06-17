"""Utilities for communicating with the ECU."""

import time
import logging
from collections import defaultdict
from threading import RLock
from ftd2xx import ftd2xx
import ftd2xx.defines as FT

from .vin_utils import vin_to_str

_LOGGER = logging.getLogger()
_LOCKS = defaultdict(RLock)
_SUPPORTED_HW = ("1406464")

class Ecu:

    def __init__(self):
        self._device = ftd2xx.open()
        self._device.setBaudRate(9600)
        self._device.setDataCharacteristics(FT.BITS_8, FT.STOP_BITS_2, FT.PARITY_EVEN)
        self._device.setFlowControl(FT.FLOW_NONE, 0, 0)
        self._device.setTimeouts(1000, 5000)

        ftdi_info = self._device.getDeviceInfo()
        _LOGGER.info("Using FTDI device: %s (%s)", ftdi_info["description"], ftdi_info["serial"])
        self._lock = _LOCKS[ftdi_info["serial"]]

        hw_info = self.getHardwareVersion()
        if not hw_info:
            raise Exception("Unable to communicate with ECU")

        if hw_info not in _SUPPORTED_HW:
            raise Exception("Device not supported")

    def _send(self, buf):
        self._device.write(buf)
        # Wait for Tx buffer to be empty
        while self._device.getStatus()[1] != 0:
            time.sleep(0.01)

    def _recv(self, length):
        buf = b""
        for attempt in range(0, 5):
            buf += self._device.read(length - len(buf))
            if len(buf) >= length:
                break
        return buf

    def getHardwareVersion(self):
        """Get the hardware version"""
        with self._lock:
            self._send(b"\x12\x04\x00\x16")
            return self._recv(50)[7:14].decode()

    def getVin(self):
        """Get the VIN programmed into the bootloader"""
        with self._lock:
            self._send(b"\x12\x09\x06\x00\x00\x1d\x07\x0d\x0a")
            return vin_to_str(self._recv(26)[12:25])
