import os
import click

from pyms41 import rom_utils

@click.group(help="Utilities for working with MS41 ECU rom and .bin files")
def rom():
    pass


@rom.command(help="Converts between ECU .bin and .mem files for disassembly")
@click.argument("filename", required=True)
def convert(filename):
    if os.path.getsize(filename) != 262144:
        click.echo("Wrong file size!", err=True)
        exit(1)

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
