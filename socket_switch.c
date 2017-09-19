#include <stdlib.h>
#include <stdio.h>
#include <wiringPi.h>

int main(int argc, char *argv[]) {
    // First and only argument is socket to switch:
    if (argc < 2 || argc > 2) {
        printf("Expected exactly one argument (the socket), got %d!\n", argc-1);
        return 1;
    }
    int socket = atoi(argv[1]);
    // Get code for the given socket (A=1, …, D=4):
    if (socket < 1 || socket > 4) {
        printf("Only argument has to be the socket number (1 … 4)!\n"); 
        return 1;
    }
    unsigned long codes[] = {340, 1108, 1348, 1300};
    unsigned long code = codes[socket-1];
    // Set up wiringPi library and pin to use:
    if (wiringPiSetup() == -1) {
        printf("Failed to setup wiringPi!\n");
        return 1;
    }
    pinMode(0, OUTPUT);
    // Transmit the code:
    printf("Sending code '%d'.\n", code);
    for (int repeat = 0; repeat < 10; repeat++) {
        for (int bit = 23; bit >= 0; bit--) {
            if (code & (1L << bit)) {
                // Transmit 1 bit (3 high pulses, 1 low pulse):
                digitalWrite(0, HIGH);
                delayMicroseconds(3*350);
                digitalWrite(0, LOW);
                delayMicroseconds(350);
            } else {
                // Transmit 0 bit (1 high pulse, 3 low pulses):
                digitalWrite(0, HIGH);
                delayMicroseconds(350);
                digitalWrite(0, LOW);
                delayMicroseconds(3*350);
            }
        }
        // Transmit sync bit (1 high pulse, 31 low pulses):
        digitalWrite(0, HIGH);
        delayMicroseconds(350);
        digitalWrite(0, LOW);
        delayMicroseconds(31*350);
    }
    // Return successfully:
    return 0;
}
