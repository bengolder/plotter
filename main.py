from serial.tools import list_ports

def get_plotter():
    for serial_port in list_ports.comports():
        print("\nHey a serial port thing!")
        print(serial_port.device)
        print(serial_port.name)
        print(serial_port.description)
        print(serial_port.hwid)

if __name__ == '__main__':
    get_plotter()
