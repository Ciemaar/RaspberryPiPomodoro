try:
    import RPi.GPIO as GPIO
except ImportError:
    import RPiFake.GPIO as GPIO

import time

GPIO.setmode(GPIO.BOARD)

class State(object):
    def __init__(self, name):
        self.name = name

STARTUP = State("startup")
READY = State("ready")

blink_time = time.time()
state_time = time.time()
state = STARTUP

def state_change(new_state):
    global state, state_time, button_time
    state_time = time.time()
    print "\n",state.name,"->",new_state.name,"\n"
    state = new_state

while True:

    if state is READY:
        pass
    elif state is STARTUP:
        state_change(READY  )


    print state.name,"\t\t",time.time()-state_time,"\r",
