import serial
from serial.tools import list_ports

class Plotter:
    UNITS_PER_INCH = 1018.39880656

    def __init__(self, serial):
        self.ser = serial

    def get_status(self):
        self.ser.write(b'OA;')
        return self.ser.readline()

    def up(self, *coords):
        self.ser.write(b'PU;')

    def down(self, *coords):
        self.ser.write(b'PD;')

    def feed_coords(self, *coords):
        for coord in coords:
            for value in coord:
                yield int(value * UNITS_PER_INCH)
                 
    def test_plot(self):
        self.ser.write(b'PU0,0;')
        self.ser.write(b'PD-1000,-1000,1000,-1000,1000,1000,-1000,1000,-1000,-1000;')
        self.ser.write(b'PU-3000,-1000;')
        self.ser.write(b'PD-3000,-1000,-1000,-1000,-1000,1000,-3000,1000,-3000,-1000;')


def get_plotter():
    for serial_port in list_ports.comports():
        if 'Keyspan' in serial_port.description:
            print('I found the plotter!')
            with serial.Serial(serial_port.device, timeout=0.05) as ser:
                ser.write(b'IN;')
                ser.write(b'OI;')
                result = ser.readline()
                print("It's a", result.decode('utf-8'))
                plotter = Plotter(ser)
                plotter.test_plot()




if __name__ == '__main__':
    get_plotter()

