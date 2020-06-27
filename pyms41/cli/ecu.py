import os
import click

from pyms41.ds2 import DS2
from pyms41.vin_utils import vin_to_str


@click.group(help="Interact with MS41 ECU (reading, flashing, etc)")
def ecu():
    pass


@ecu.command(help="Read basic info from ECU")
def info():
    ds2 = DS2()
    click.echo(f"HW: {ds2.identify_ecu()[:7].decode()}")
    click.echo(f"VIN: {vin_to_str(ds2.read_vin())}")


@ecu.group(help="Read/clear DTC codes")
def dtc():
    pass


@dtc.command(help="Read all DTC codes")
def list():
    ds2 = DS2()
    click.echo(ds2.read_dtc())


@dtc.command(help="Get detailed info about specific DTC code")
@click.argument("index", required=True)
def details(index):
    ds2 = DS2()
    click.echo(ds2.read_dtc(int(index)))


@dtc.command(help="Clear DTC codes")
def clear():
    ds2 = DS2()
    ds2.clear_dtc()
