import sys
import time
from RPi import GPIO


class SocketRemote:
    pin = 17
    pulse_length = 300
    repeat = 10

    def __init__(self, house_code='000000'):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.pin, GPIO.OUT, initial=GPIO.LOW)
        self.house_code = house_code

    def send_hi_lo(self, hi, lo):
        GPIO.output(self.pin, GPIO.HIGH)
        time.sleep(hi * self.pulse_length / 1000000.0)
        GPIO.output(self.pin, GPIO.LOW)
        time.sleep(lo * self.pulse_length / 1000000.0)

    def send_sync(self):
        self.send_hi_lo(1, 31)

    def send_zero(self):
        self.send_hi_lo(1, 3)

    def send_one(self):
        self.send_hi_lo(3, 1)

    def switch_socket(self, socket):
        sockets = {'A': '00010101', 'B': '01000101',
                   'C': '01010100', 'D': '01010001'}
        socket = socket.upper()
        if socket not in sockets:
            return False
        socket = sockets[socket]
        bit_string = ''
        for bit in self.house_code:
            bit_string += '0{}'.format(bit)
        bit_string += socket
        bit_string += '0100'
        for _ in range(self.repeat):
            self.send_sync()
            for bit in bit_string:
                if bit == '0':
                    self.send_zero()
                if bit == '1':
                    self.send_one()
        return True

    def close(self):
        GPIO.cleanup()


if __name__ == '__main__':
    socket = sys.argv[1]
    print("Switching socket '{}'.".format(socket))
    remote = SocketRemote()
    success = remote.switch_socket(socket)
    remote.close()
    if not success:
        print("Socket '{}' not known!.".format(socket))
