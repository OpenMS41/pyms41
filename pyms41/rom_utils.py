"""Utilities for converting MS41 .bin files to .mem files (for use in IDA/Ghidra)."""

import os


def bin_to_mem(input, output):
    """Convert .bin file to .mem file.

    :param input: Input file-like object to be converted
    :param output: Output file-like object to store result

    Example usage::

        with open('input.bin', 'rb') as input:
            with open('output.mem', 'wb') as output:
                bin_to_mem(intput, output)
    """
    # 0x00000 - 0x10000
    _block_copy(input, 0x04000, output, 0x00000, 0x4000)
    _block_copy(input, 0x00000, output, 0x04000, 0x4000)
    _block_copy(input, 0x0c000, output, 0x08000, 0x4000)
    _block_copy(input, 0x08000, output, 0x0C000, 0x4000)

    # 0x10000 - 0x2000
    _block_copy(input, 0x14000, output, 0x10000, 0x4000)
    _block_copy(input, 0x10000, output, 0x14000, 0x4000)
    _block_copy(input, 0x1c000, output, 0x18000, 0x4000)
    _block_copy(input, 0x18000, output, 0x1C000, 0x4000)

    # 0x20000 - 0x3000
    _block_copy(input, 0x24000, output, 0x20000, 0x4000)
    _block_copy(input, 0x20000, output, 0x24000, 0x4000)
    _block_copy(input, 0x2c000, output, 0x28000, 0x4000)
    _block_copy(input, 0x28000, output, 0x2C000, 0x4000)

    # 0x30000 - 0x4000
    _block_copy(input, 0x34000, output, 0x30000, 0x4000)
    _block_copy(input, 0x30000, output, 0x34000, 0x4000)
    _block_copy(input, 0x3c000, output, 0x38000, 0x4000)
    _block_copy(input, 0x38000, output, 0x3C000, 0x4000)


def mem_to_bin(input, output):
    """Convert .mem file to .bin file.

    :param input: Input file-like object to be converted
    :param output: Output file-like object to store result

    Example usage::

        with open('input.mem', 'rb') as input:
            with open('output.bin', 'wb') as output:
                mem_to_bin(intput, output)
    """
    # 0x00000 - 0x10000
    _block_copy(input, 0x00000, output, 0x04000, 0x4000)
    _block_copy(input, 0x04000, output, 0x00000, 0x4000)

    # fill up space used by ram with ff`s
    _fill(output, 0x08000, 0x0c000, b"\xff")

    _block_copy(input, 0x08000, output, 0x0C000, 0x4000)

    # 0x10000 - 0x20000
    _block_copy(input, 0x10000, output, 0x14000, 0x4000)
    _block_copy(input, 0x14000, output, 0x10000, 0x4000)

    _fill(output, 0x18000, 0x20000, b"\xff")

    # 0x20000 - 0x30000
    _block_copy(input, 0x20000, output, 0x24000, 0x4000)
    _block_copy(input, 0x24000, output, 0x20000, 0x4000)
    _block_copy(input, 0x28000, output, 0x2C000, 0x4000)
    _block_copy(input, 0x2C000, output, 0x28000, 0x4000)

    # 0x30000 - 0x40000
    _block_copy(input, 0x30000, output, 0x34000, 0x4000)
    _block_copy(input, 0x34000, output, 0x30000, 0x4000)
    _block_copy(input, 0x38000, output, 0x3C000, 0x4000)
    _block_copy(input, 0x3C000, output, 0x38000, 0x4000)


def _fill(fd, start, end, b):
    fd.seek(start)
    fd.write(b * (end - start))


def _block_copy(input, in_start, output, out_start, length):
    input.seek(in_start)
    output.seek(out_start)
    output.write(input.read(length))
