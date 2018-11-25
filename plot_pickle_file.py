import pickle
import click
import serial
from serial.tools import list_ports

class Plotter:
    UNITS_PER_INCH = 1018.39880656

    def __init__(self, serial):
        self.ser = serial

    def get_status(self):
        self.ser.write(b'OA;')
        return self.ser.readline()

    def feed_coords(self, *coords):
        for coord in coords:
            for value in coord:
                yield str(int(value * self.UNITS_PER_INCH))

    def write_to_serial(self, command_string, dryrun=True):
        if dryrun:
            click.echo('SERIAL COMMAND: ' + command_string)
        else:
            self.ser.write(command_string.encode('utf-8'))

    def up(self, *coords):
        self.write_to_serial('PU' + ','.join(self.feed_coords(*coords)))

    def down(self, *coords):
        self.write_to_serial('PD' + ','.join(self.feed_coords(*coords)))

    def plot_geom(self, geom):
        self.up(geom[0])
        self.down(*geom)

    def plot_geom_list(self, geoms):
        for geom in geoms:
            self.plot_geom(geom)

    def test_plot(self):
        self.ser.write(b'PU0,0;')
        self.ser.write(b'PD-1000,-1000,1000,-1000,1000,1000,-1000,1000,-1000,-1000;')
        self.ser.write(b'PU-3000,-1000;')
        self.ser.write(b'PD-3000,-1000,-1000,-1000,-1000,1000,-3000,1000,-3000,-1000;')

@click.command()
@click.argument('picklefile', type=click.File('rb'))
def plot(picklefile):
    for serial_port in list_ports.comports():
        if 'Keyspan' in serial_port.description:
            print('I found the plotter!')
            with serial.Serial(serial_port.device, timeout=0.05) as ser:
                ser.write(b'IN;')
                ser.write(b'OI;')
                result = ser.readline()
                print("It's a", result.decode('utf-8'))
                plotter = Plotter(ser)
                plotter.plot_geom_list(pickle.load(picklefile))


if __name__ == '__main__':
    print("Running")
    plot()

