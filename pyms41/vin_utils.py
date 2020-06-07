"""Utilities for converting VIN to/from MS41 hex format."""

import string
import struct

_CHAR_MAP = list(string.digits + string.ascii_uppercase)


def vin_to_str(vin: bytes) -> str:
    """Convert VIN from MS41 bytes to string.

        :param vin: Bytes representing the VIN as stored in MS41
        :returns: VIN as human readable string
        :rtype: str

        Example usage::

            >>> vin_to_str(b"\x20\x2C\xA3\x4D\x0C\x10\x08\x00\xB7\x82\x10\x70\x87")
            'WBADD31080BU24727'
    """
    padded_vin = vin.rjust(15, b"\x00")
    return "".join(
        _CHAR_MAP[(x >> 18) & 63] + _CHAR_MAP[(x >> 12) & 63] + _CHAR_MAP[(x >> 6) & 63] + _CHAR_MAP[x & 63]
        for x in [
            (x1 << 16) | (x2 << 8) | x3
            for x1, x2, x3 in _chunk(padded_vin, 3)
        ]
    )[3:]


def vin_to_bytes(vin: str) -> bytes:
    """Convert VIN from string to MS41 bytes.

        :param vin: VIN as human readable string
        :returns: Bytes representing the VIN as stored in MS41
        :rtype: bytes

        Example usage::

            >>> vin_to_bytes("WBADD31080BU24727")
            b'\x20\x2C\xA3\x4D\x0C\x10\x08\x00\xB7\x82\x10\x70\x87'
    """
    vin_bytes = bytes([_CHAR_MAP.index(x) for x in vin.upper()]).rjust(20, b"\x00")
    return b"".join(
        bytes([x >> 16, (x >> 8) & 0xff, x & 0xff])
        for x in [
            (x1 << 18) | (x2 << 12) | (x3 << 6) | x4
            for x1, x2, x3, x4 in _chunk(vin_bytes, 4)
        ]
    )[2:]


def _chunk(l, size):
    return [
        l[i:i + size]
        for i in range(0, len(l), size)
    ]
