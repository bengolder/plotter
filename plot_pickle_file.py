import pickle
import click
import serial
from serial.tools import list_ports

class Plotter:
    UNITS_PER_INCH = 1018.39880656

    def __init__(self, serial, send_to_plotter=False, verbose=False):
        self.ser = serial
        self.send_to_plotter = send_to_plotter and serial
        self.verbose = verbose

    def feed_coords(self, *coords):
        for coord in coords:
            for value in coord:
                yield str(int(value * self.UNITS_PER_INCH))

    def write_to_serial(self, command_string):
        if self.verbose:
            click.echo(command_string)
        if self.send_to_plotter:
            self.ser.write(command_string.encode('utf-8'))

    def up(self, *coords):
        self.write_to_serial('PU' + ','.join(self.feed_coords(*coords)) + ';')

    def down(self, *coords):
        self.write_to_serial('PD' + ','.join(self.feed_coords(*coords)) + ';')

    def plot_geom(self, geom):
        self.up(geom[0])
        self.down(*geom)

    def plot_geom_list(self, geoms):
        for geom in geoms:
            self.plot_geom(geom)


@click.command()
@click.argument('picklefile', type=click.File('rb'))
@click.option('-v', '--verbose', default=False, is_flag=True,
    help='Echo all HPGL commands to STDOUT.')
@click.option('-s', '--send', default=False, is_flag=True,
    help='Send all commands to the plotter. Without this flag, only a preview will be produced.')
def plot(picklefile, verbose=False, send=False):
    '''This script plots a python PICKLEFILE in pickle protocol containing a list of coordinate lists.
    '''
    if send:
        for serial_port in list_ports.comports():
            if 'Keyspan' in serial_port.description:
                print('I found the plotter!')
                with serial.Serial(serial_port.device, timeout=0.05, xonxoff=True) as ser:
                    ser.write(b'IN;')
                    ser.write(b'OI;')
                    result = ser.readline()
                    print("It's a", result.decode('utf-8'))
                    plotter = Plotter(ser, send_to_plotter=send, verbose=verbose)
                    data = pickle.load(picklefile)
                    plotter.plot_geom_list(data)
    else:
        plotter = Plotter(None, send_to_plotter=send, verbose=verbose)
        data = pickle.load(picklefile)
        plotter.plot_geom_list(data)


if __name__ == '__main__':
    plot()

