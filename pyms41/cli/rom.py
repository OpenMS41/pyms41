import os
import click

from pyms41.rom_utils import Rom

@click.group(help="Tools for manipulating .bin/.rom files")
def rom():
    pass


@rom.command(help="Correct crc16 checksums in rom")
@click.argument("filename", required=True)
def checksum(filename):
    rom = Rom.from_bin(filename)


@rom.command(help="Converts between ECU .bin and .mem files for disassembly")
@click.argument("filename", required=True)
def convert(filename):
    rom_utils.verify_rom_file(filename)

    file, ext = os.path.splitext(filename)
    with open(filename, "rb") as i:
        i.seek(0x14000)
        if i.read(1) == b"\x4e":
            out_filename = file + ".mem"
            click.echo(f"Detected file as .bin format, writing .mem output to: {out_filename}")
            with open(out_filename, 'wb') as o:
                rom_utils.bin_to_mem(i, o)
                exit(0)

        i.seek(0x10000)
        if i.read(1) == b"\x4e":
            out_filename = file + ".bin"
            click.echo(f"Detected file as .mem format, writing .bin output to: {out_filename}")
            with open(out_filename, 'wb') as o:
                rom_utils.mem_to_bin(i, o)
                exit(0)

        click.echo("File not valid .bin or .mem/.rom", err=True)
        exit(1)
