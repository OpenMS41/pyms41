import logging
from collections import defaultdict
from enum import IntEnum
from threading import RLock

from ftd2xx import ftd2xx
from ftd2xx.ftd2xx import FTD2XX
import ftd2xx.defines as FT


_LOGGER = logging.getLogger()
_LOCKS = defaultdict(RLock)


def _checksum(buf: bytes) -> int:
    calculated_sum = buf[0]
    for x in buf[1:]:
        calculated_sum ^= x
    return calculated_sum


def _verify(buf: bytes) -> bool:
    return _checksum(buf[:-1]) == buf[-1]


class DS2Commands(IntEnum):
    IDENTIFY = 0
    READ_DTC = 4
    CLEAR_DTC = 5
    READ_MEM = 6


class DS2:

    def __init__(self, device: FTD2XX = None):
        if device is None:
            device = ftd2xx.open()
        self._device = device
        self._device.setBaudRate(9600)
        self._device.setDataCharacteristics(FT.BITS_8, FT.STOP_BITS_2, FT.PARITY_EVEN)
        self._device.setFlowControl(FT.FLOW_NONE, 0, 0)
        self._device.setTimeouts(1000, 5000)

        ftdi_info = self._device.getDeviceInfo()
        # _LOGGER.info("Using FTDI device: %s (%s)", ftdi_info["description"], ftdi_info["serial"])
        self._lock = _LOCKS[ftdi_info["serial"]]

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

    def _execute_command(self, addr, command, args = b""):
        with self._lock:
            # send command
            request = bytes([addr, len(args) + 4, command]) + args
            request += bytes([_checksum(request)])
            self._send(request)

            # read response
            self._recv(len(request))
            addr, length = self._recv(2)
            response = bytes([addr, length]) + self._recv(length - 2)
            if not _verify(response):
                raise InvalidChecksumException()
            return response[3:-1]

    def identify_ecu(self):
        return self._execute_command(0x12, DS2Commands.IDENTIFY)

    def read_dtc(self, specific_fault=1):
        return self._execute_command(0x12, DS2Commands.READ_DTC, bytes([specific_fault]))

    def clear_dtc(self):
        return self._execute_command(0x12, DS2Commands.CLEAR_DTC)

    def read_vin(self):
        return self._execute_command(0x12, DS2Commands.READ_MEM, bytes([0, 0, 0x1d, 0x07, 13]))


class InvalidChecksumException(Exception):
    """Raised when an invalid checksum is encountered."""
