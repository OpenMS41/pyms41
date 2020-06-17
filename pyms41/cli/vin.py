import os
import click
from pyms41 import vin_utils

@click.command(help="Convert VIN between ascii and MS41 hex")
@click.argument("vin", required=True)
def vin(vin):
    vin_bytes = None

    if len(vin) == 17:
        click.echo("Converting VIN to MS41 bytes")
        result = ("0x" + "{:02x}" * 13).format(*vin_utils.vin_to_bytes(vin))
        click.echo(result)
        exit(0)

    if vin.startswith("0x") and len(vin) == 28:
        vin_bytes = bytes.fromhex(vin[2:])
    elif len(vin) == 13:
        click.echo("Encoding not clear, attempting to decode VIN as MS41 bytes")
        vin_bytes = vin.encode("utf-8")

    if vin_bytes is not None:
        result = vin_utils.vin_to_str(vin_bytes)
        click.echo(result)
        exit()

    click.echo("Invalid VIN. Must be 17 characters long.")
    exit(1)
