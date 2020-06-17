"""Utilities for converting MS41 .bin files to .mem files (for use in IDA/Ghidra)."""

import os
from io import BytesIO
import struct
import logging
import click
from .crc16 import crc

_FILE_SIZE = 262144
_LOGGER = logging.getLogger()


class Rom:

    def __init__(self, mem_bytes):
        if len(mem_bytes) != _FILE_SIZE:
            raise InvalidRom(f"File size incorrect. Got {len(mem_bytes)}, expected {_FILE_SIZE}")

        self._bytes = mem_bytes

        # Verify checksums
        if self._get_boot_loader_checksum() != self._calc_boot_loader_checksum():
            _LOGGER.warning("Boot loader checksum invalid")

        # Not working yet... something is not quite right
        # if self._get_program_checksum() != self._calc_program_checksum():
        #     _LOGGER.warning("Program checksum invalid")

    @staticmethod
    def from_bin(filename):
        with open(filename, 'rb') as fd:
            # Read .bin with corrected memory addresses
            contents = b"".join(
                _read(fd, start, 0x4000)
                for start in [
                    0x04000, 0x00000, 0x0c000, 0x08000,
                    0x14000, 0x10000, 0x1c000, 0x18000,
                    0x24000, 0x20000, 0x2c000, 0x28000,
                    0x34000, 0x30000, 0x3c000, 0x38000,
                ]
            )
            return Rom(contents)

    @staticmethod
    def from_mem(filename):
        with open(filename, 'rb') as fd:
            return Rom(fd.read())

    def _get_boot_loader_checksum(self):
        return self._bytes[0x1C80:0x1C82]

    def _calc_boot_loader_checksum(self):
        initial_value = 0x4711
        return _checksum(self._bytes, initial_value, (0x0000, 0x1C14))

    def _get_program_checksum(self):
        return self._bytes[0x2050:0x2052]

    def _calc_program_checksum(self):
        initial_value = struct.unpack('<H', self._bytes[0x2066:0x2068])[0]
        sections_to_calculate = [
            (0x02100, _find_checksum_end(self._bytes, 0x3fff)),
            (0x04000, _find_checksum_end(self._bytes, 0x7fff)),
            (0x20000, _find_checksum_end(self._bytes, 0x3ffff)),
        ]
        return _checksum(self._bytes, initial_value, *sections_to_calculate)


    def to_bin(self):
        fd = BytesIO()
        fd.write(self._bytes[0x04000:0x04000 + 0x40000])
        fd.write(self._bytes[0x00000:0x00000 + 0x40000])

        # fill up space used by ram with ff`s
        fd.write(b"\xff" * (0x0c000 - fd.tell()))

        fd.write(self._bytes[0x08000:0x08000 + 0x4000])

        # 0x10000 - 0x20000
        fd.write(self._bytes[0x14000:0x14000 + 0x4000])
        fd.write(self._bytes[0x10000:0x10000 + 0x4000])

        fd.write(b"\xff" * (0x20000 - fd.tell()))

        # 0x20000 - 0x30000
        fd.write(self._bytes[0x24000:0x24000 + 0x4000])
        fd.write(self._bytes[0x20000:0x20000 + 0x4000])
        fd.write(self._bytes[0x2C000:0x2C000 + 0x4000])
        fd.write(self._bytes[0x28000:0x28000 + 0x4000])

        # 0x30000 - 0x40000
        fd.write(self._bytes[0x34000:0x34000 + 0x4000])
        fd.write(self._bytes[0x30000:0x30000 + 0x4000])
        fd.write(self._bytes[0x3C000:0x3C000 + 0x4000])
        fd.write(self._bytes[0x38000:0x38000 + 0x4000])

        return fd.getvalue()

    def to_mem(self):
        return self._bytes[:]


class InvalidRom(ValueError):
    """Raised when invalid rom is passed"""


def _read(fd, start, length):
    fd.seek(start)
    return fd.read(length)


def _checksum(buf, initial_value, *locations):
    sum = initial_value
    for start, end in locations:
        sum = crc(buf[start:end], sum)

    return struct.pack('<H', sum)


def _find_checksum_end(buf, start):
    end = start
    while buf[end] == b"\xff":
        end -= 1
    return end + 1
