import click
from serial.tools import list_ports

@click.command()
def detect():
    """Lists serial ports"""
    for i, serial_port in enumerate(list_ports.comports()):
    	count = i + 1
    	click.echo("Found {0} serial device:".format(count))
    	click.echo("\tDevice: {0}".format(serial_port.device))
    	click.echo("\tName: {0}".format(serial_port.name))
    	click.echo("\tDescription: {0}".format(serial_port.description))
    	click.echo("\tManufacturer: {0}".format(serial_port.manufacturer))
    	click.echo("\tSerial number: {0}".format(serial_port.serial_number))
    	click.echo("\tHWID: {0}".format(serial_port.hwid))
    	click.echo("\tPID: {0}".format(serial_port.pid))

if __name__ == '__main__':
    detect()