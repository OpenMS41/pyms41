import os
import click

from pyms41.ecu_utils import Ecu

@click.group(help="Interact with MS41 ECU (reading, flashing, etc)")
def ecu():
    pass


@ecu.command(help="Read basic info from ECU")
def info():
    ecu = Ecu()
    click.echo(f"HW: {ecu.getHardwareVersion()}")
    click.echo(f"VIN: {ecu.getVin()}")
