try:
    import RPi.GPIO as GPIO
except ImportError:
    import RPiFake.GPIO as GPIO

import time
from collections import deque

GPIO.setmode(GPIO.BOARD)

class State(object):
    def __init__(self, name):
        self.name = name

STARTUP = State("startup")
READY = State("ready")

blink_time = time.time()
state_time = time.time()
state = STARTUP

loop_time = time.time()
loop_times = deque(maxlen=20)

def state_change(new_state, time_at):
    global state, state_time, button_time
    state_time = time_at
    print "\n",state.name,"->",new_state.name,"\n"
    state = new_state

while True:
    last_loop = loop_time
    loop_time = time.time()
    if state is READY:
        pass
    elif state is STARTUP:
        state_change(READY,loop_time)

    print state.name,"\t\t",loop_time-state_time,"\tLoop Time",loop_time-last_loop,"\r",
    #loop_times.append(loop_time-last_loop)
    #print "Max Loop",max(loop_times),"\tMin loop",min(loop_times),"\tAvg Loop",sum(loop_times)/len(loop_times),"\r",