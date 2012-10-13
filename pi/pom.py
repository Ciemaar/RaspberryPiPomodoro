import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(11, GPIO.IN)

class State(object):
    def __init__(self, name):
        self.name = name

STARTUP = State("startup")
READY = State("ready")
POM = State("pom")
BREAK = State("break")
BREAK_END = State("breakend")

blink_time = time.time()
button_time = None
state_time = time.time()
state = STARTUP
led_on = False
led_curr = False
delay = 0
SHORT_PUSH = .02
LONG_PUSH = 1
accel = 1.0
POM_TIME = 25*60 * accel
BREAK_TIME = 5*60 * accel
WARN_TIME = 2*60 * accel

def state_change(new_state):
    global state, state_time, button_time
    state_time = time.time()
    print "\n",state.name,"->",new_state.name,"\n"
    state = new_state
    button_time = time.time() + 3 * LONG_PUSH

while True:
    pushed = 0
    if button_time:
        pushed = time.time() - button_time
        if GPIO.input(11):
            button_time = None
            if pushed < SHORT_PUSH:
                pushed = 0
        elif pushed < LONG_PUSH:
                pushed = 0
    elif not GPIO.input(11):
        button_time = time.time()
        pushed = 0

    if state is READY:
        led_on = False
        if pushed:
            state_change(POM)
    elif state is POM:
        led_on = True
        if time.time() - state_time > POM_TIME:
            state_change(BREAK)
        if pushed>LONG_PUSH:
            state_change(READY)
    elif state is BREAK:
        if time.time() > blink_time + (1 if led_on else 2):
            led_on = not led_on
            blink_time = time.time()
        if (time.time() - state_time) > (BREAK_TIME - WARN_TIME):
            state_change(BREAK_END)
        if not pushed:
            pass
        elif pushed<LONG_PUSH:
            state_change(READY)
        else:
            state_change(POM)
    elif state is BREAK_END:
        if time.time() > blink_time + .2:
            led_on = not led_on
            blink_time = time.time()
        if time.time() - state_time > WARN_TIME:
            state_change(READY)
        if pushed:
            state_change(POM)
    elif state is STARTUP:
        if time.time() > blink_time + .02:
            led_on = not led_on
            blink_time = time.time()
        if time.time() - state_time > 5:
            state_change(READY)
        if pushed:
	    accel = .1
	    POM_TIME = 60 * accel
	    BREAK_TIME = 5*60 * accel
	    WARN_TIME = 2*60 * accel

    if led_on != led_curr:
      led_curr = led_on
      GPIO.output(12, led_curr)

    print state.name,"\t\t",time.time()-state_time, pushed,"\r",
