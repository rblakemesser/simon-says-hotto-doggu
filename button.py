import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

buttons = {
        15: 'red',
        18: 'yellow',
}


def cb(p):
    print(buttons[p])


for pin, color in buttons.items():
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(pin, GPIO.RISING, callback=cb)


input('press enter to quit\n\n')

GPIO.cleanup()
#while True:
#    red_state = GPIO.input(RED)
#    if not red_state:
#        print("Red Button Pressed")
#        time.sleep(.3)
#
#    yellow_state = GPIO.input(YELLOW)
#    if not yellow_state:
#        print("Yellow Button Pressed")
#        time.sleep(.3)



