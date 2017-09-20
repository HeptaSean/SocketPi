import sys
import wiringpi

PIN = 0
PULSE_LENGTH = 350
BITS = 24
REPEAT = 10

wiringpi.wiringPiSetup()
wiringpi.pinMode(PIN, 1)

def send_code(code):
    bits = format(code, '0{}b'.format(BITS))
    for _ in range(REPEAT):
        for bit in bits:
            if bit == '0':
                wiringpi.digitalWrite(PIN, 1)
                wiringpi.delayMicroseconds(  PULSE_LENGTH)
                wiringpi.digitalWrite(PIN, 0)
                wiringpi.delayMicroseconds(3*PULSE_LENGTH)
            if bit == '1':
                wiringpi.digitalWrite(PIN, 1)
                wiringpi.delayMicroseconds(3*PULSE_LENGTH)
                wiringpi.digitalWrite(PIN, 0)
                wiringpi.delayMicroseconds(  PULSE_LENGTH)
        wiringpi.digitalWrite(PIN, 1)
        wiringpi.delayMicroseconds(   PULSE_LENGTH)
        wiringpi.digitalWrite(PIN, 0)
        wiringpi.delayMicroseconds(31*PULSE_LENGTH)

if __name__ == '__main__':
    codes = {'A': 340, 'B': 1108, 'C': 1348, 'D': 1300}

    argc = len(sys.argv) - 1
    if argc < 1 or argc > 1:
        print("Expected exactly one argument (the socket), " +
                "got {}!".format(argc))
        exit(1)

    socket = sys.argv[1].upper()
    if not socket in codes:
        print("Socket {} not known!".format(socket))
        exit(1)

    code = codes[socket]
    print("Sending code '{}'.".format(code))
    send_code(code)
