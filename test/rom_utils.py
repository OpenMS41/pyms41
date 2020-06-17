from io import BytesIO
from os import path
from unittest import TestCase

from pyms41.rom_utils import Rom


class RomTest(TestCase):
    def test_checksums(self):
        rom = Rom.from_bin(path.dirname(__file__) + "/resources/test.bin")
        self.assertEqual(rom._get_boot_loader_checksum(), rom._calc_boot_loader_checksum())
        # this one is still broken
        # self.assertEqual(rom._get_program_checksum(), rom._calc_program_checksum())

    def test_conversions(self):
        bin_rom = Rom.from_bin(path.dirname(__file__) + "/resources/test.bin")
        mem_rom = Rom(bin_rom.to_mem())

        self.assertEqual(bin_rom.to_bin(), mem_rom.to_bin())
        self.assertEqual(bin_rom.to_mem(), mem_rom.to_mem())
