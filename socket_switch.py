import sys
import time
from RPi import GPIO

PIN = 17
PULSE_LENGTH = 350
BITS = 24
REPEAT = 10
CODES = {'A': 340, 'B': 1108, 'C': 1348, 'D': 1300}

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setwarnings(False)

def send_code(code):
    bits = format(code, '0{}b'.format(BITS))
    for _ in range(REPEAT):
        GPIO.output(PIN, GPIO.HIGH)
        time.sleep(   PULSE_LENGTH/1000000.0)
        GPIO.output(PIN, GPIO.LOW)
        time.sleep(31*PULSE_LENGTH/1000000.0)
        for bit in bits:
            if bit == '0':
                GPIO.output(PIN, GPIO.HIGH)
                time.sleep(  PULSE_LENGTH/1000000.0)
                GPIO.output(PIN, GPIO.LOW)
                time.sleep(3*PULSE_LENGTH/1000000.0)
            if bit == '1':
                GPIO.output(PIN, GPIO.HIGH)
                time.sleep(3*PULSE_LENGTH/1000000.0)
                GPIO.output(PIN, GPIO.LOW)
                time.sleep(  PULSE_LENGTH/1000000.0)

if __name__ == '__main__':
    argc = len(sys.argv) - 1
    if argc < 1 or argc > 1:
        print("Expected exactly one argument (the socket), " +
                "got {}!".format(argc))
        exit(1)

    socket = sys.argv[1].upper()
    if not socket in CODES:
        print("Socket {} not known!".format(socket))
        exit(1)

    code = CODES[socket]
    print("Sending code '{}'.".format(code))
    send_code(code)
    GPIO.cleanup()
