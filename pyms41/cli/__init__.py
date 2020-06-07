import click

from .rom import rom
from .vin import vin


@click.group()
def cli():
    pass


cli.add_command(rom)
cli.add_command(vin)


if __name__ == "__main__":
    cli()
