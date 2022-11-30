from gpiozero import DigitalOutputDevice
import time


class Broche(DigitalOutputDevice):
    pass


LSBFIRST = 1
MSBFIRST = 2

dataPin = Broche(17)
latchPin = Broche(27)
clockPin = Broche(22)
data = {
    " ": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    "0": [0x00, 0x00, 0x3E, 0x41, 0x41, 0x3E, 0x00, 0x00],
    "1": [0x00, 0x00, 0x21, 0x7F, 0x01, 0x00, 0x00, 0x00],
    "2": [0x00, 0x00, 0x23, 0x45, 0x49, 0x31, 0x00, 0x00],
    "3": [0x00, 0x00, 0x22, 0x49, 0x49, 0x36, 0x00, 0x00],
    "4": [0x00, 0x00, 0x0E, 0x32, 0x7F, 0x02, 0x00, 0x00],
    "5": [0x00, 0x00, 0x79, 0x49, 0x49, 0x46, 0x00, 0x00],
    "6": [0x00, 0x00, 0x3E, 0x49, 0x49, 0x26, 0x00, 0x00],
    "7": [0x00, 0x00, 0x60, 0x47, 0x48, 0x70, 0x00, 0x00],
    "8": [0x00, 0x00, 0x36, 0x49, 0x49, 0x36, 0x00, 0x00],
    "9": [0x00, 0x00, 0x32, 0x49, 0x49, 0x3E, 0x00, 0x00],
    "A": [0x00, 0x00, 0x3F, 0x44, 0x44, 0x3F, 0x00, 0x00],
    "B": [0x00, 0x00, 0x7F, 0x49, 0x49, 0x36, 0x00, 0x00],
    "C": [0x00, 0x00, 0x3E, 0x41, 0x41, 0x22, 0x00, 0x00],
    "D": [0x00, 0x00, 0x7F, 0x41, 0x41, 0x3E, 0x00, 0x00],
    "E": [0x00, 0x00, 0x7F, 0x49, 0x49, 0x41, 0x00, 0x00],
    "F": [0x00, 0x00, 0x7F, 0x48, 0x48, 0x40, 0x00, 0x00],
    "G": [0x00, 0x00, 0x7F, 0x41, 0x49, 0x4F, 0x00, 0x00],
    "H": [0x00, 0x00, 0x7F, 0x8, 0x8, 0x7F, 0x00, 0x00],
    "I": [0x00, 0x00, 0x41, 0x7F, 0x7F, 0x41, 0x00, 0x00],
    "J": [0x00, 0x00, 0x46, 0x41, 0x7E, 0x40, 0x00, 0x00],
    "K": [0x00, 0x00, 0x7F, 0x8, 0x36, 0x41, 0x00, 0x00],
    "L": [0x00, 0x00, 0x7F, 0x1, 0x1, 0x1, 0x00, 0x00],
    "M": [0x00, 0x00, 0x7F, 0x20, 0x20, 0x7F, 0x00, 0x00],
    "N": [0x00, 0x00, 0x7F, 0x38, 0x1C, 0x7F, 0x00, 0x00],
    "O": [0x00, 0x00, 0x7F, 0x41, 0x41, 0x7F, 0x00, 0x00],
    "P": [0x00, 0x00, 0x7F, 0x48, 0x48, 0x78, 0x00, 0x00],
    "Q": [0x00, 0x00, 0x78, 0x48, 0x48, 0x7F, 0x00, 0x00],
    "R": [0x00, 0x00, 0x7F, 0x4C, 0x4A, 0x79, 0x00, 0x00],
    "S": [0x00, 0x00, 0x79, 0x49, 0x49, 0x4F, 0x00, 0x00],
    "T": [0x00, 0x00, 0x40, 0x7F, 0x7F, 0x40, 0x00, 0x00],
    "U": [0x00, 0x00, 0x7F, 0x1, 0x1, 0x7F, 0x00, 0x00],
    "V": [0x00, 0x00, 0x7C, 0x3, 0x3, 0x7C, 0x00, 0x00],
    "W": [0x00, 0x00, 0x7F, 0x2, 0x2, 0x7F, 0x00, 0x00],
    "X": [0x00, 0x00, 0x63, 0x1C, 0x1C, 0x63, 0x00, 0x00],
    "Y": [0x00, 0x00, 0x78, 0xF, 0xF, 0x78, 0x00, 0x00],
    "Z": [0x00, 0x00, 0x47, 0x4D, 0x59, 0x71, 0x00, 0x00],
    "0": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
}


def shiftOut(order, val):
    for i in range(0, 8):
        clockPin.off()
        if (order == LSBFIRST):
            if (0x01 & (val >> i) == 0x01):
                dataPin.on()
            else:
                dataPin.off()
        elif (order == MSBFIRST):
            if (0x80 & (val << i) == 0x80):
                dataPin.on()
            else:
                dataPin.off()
        clockPin.on()


def write(message):
    message_array = data[" "].copy()

    for letter in message.upper():
        if letter not in data:
            return

        message_array += data[letter].copy()

    for k in range(0, len(message_array)-8):
        for j in range(0, 20):
            x = 0x80
            for i in range(k, k+8):
                latchPin.off()
                shiftOut(MSBFIRST, message_array[i])
                shiftOut(MSBFIRST, ~x)
                latchPin.on()
                time.sleep(0.001)
                x >>= 1


if __name__ == '__main__':
    pass
