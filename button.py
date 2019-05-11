import time
import threading
import pygame.mixer as mix
import RPi.GPIO as GPIO


button_map = {
    14: 'green',
    15: 'red',
    18: 'yellow',
    23: 'blue',
}

sound_map = {
    'green': 'green.mp3',
    'red': 'red.mp3',
    'yellow': 'yellow.mp3',
    'blue': 'blue.mp3',
}

def beep(audio_file):
    path = "/home/pi/workspace/simon-says-hotto-doggu/assets/audio/{}".format(audio_file)
    mix.music.load(path)
    mix.music.play()


def on_press(p):
    color = button_map.get(p)
    if not color:
        return

    afile = sound_map.get(color)
    print('pressed {}'.format(color))
    beep(afile)


class ButtonHandler(threading.Thread):
    def __init__(self, pin, func, edge='both', bouncetime=200):
        super().__init__(daemon=True)

        self.edge = edge
        self.func = func
        self.pin = pin
        self.bouncetime = float(bouncetime)/1000

        self.lastpinval = GPIO.input(self.pin)
        self.lock = threading.Lock()

    def __call__(self, *args):
        if not self.lock.acquire(blocking=False):
            return

        t = threading.Timer(self.bouncetime, self.read, args=args)
        t.start()

    def read(self, *args):
        pinval = GPIO.input(self.pin)

        if (
                ((pinval == 0 and self.lastpinval == 1) and
                 (self.edge in ['falling', 'both'])) or
                ((pinval == 1 and self.lastpinval == 0) and
                 (self.edge in ['rising', 'both']))
        ):
            self.func(*args)

        self.lastpinval = pinval
        self.lock.release()


def init_buttons(button_map):
    for pin, color in button_map.items():
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        cb = ButtonHandler(pin, on_press, edge='rising', bouncetime=50)
        cb.start()
        GPIO.add_event_detect(pin, GPIO.RISING, callback=cb)


while __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    init_buttons(button_map)
    mix.init()

    input('press enter to quit\n\n')

    GPIO.cleanup()

