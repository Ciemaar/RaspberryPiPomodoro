try:
    import RPi.GPIO as GPIO
except ImportError:
    import RPiFake.GPIO as GPIO

import time
from collections import deque

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.IN)
GPIO.setup(12,GPIO.IN)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)
GPIO.output(13,True)
GPIO.output(15,True)

class State(object):
    def __init__(self, name):
        self.name = name

STARTUP = State("startup")
READY = State("ready")
SENSOR_2 = State("reading second sensor")
RESET_1 = State("resetting")
RESET_2 = State("reset complete")
CALCULATE = State("calucating delay")

blink_time = time.time()
state_time = time.time()

pwm_on = time.time()
pwm_off = time.time()
pwm_state = True

tgt_on = .8
tgt_off =  .2

sensor1 = 0
sensor2 = 0

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
    if pwm_state:
        if loop_time - pwm_on >= tgt_on:
            pwm_off = loop_time
            pwm_state = False
            GPIO.output(15,not pwm_state)
    else:
        if loop_time - pwm_off >= tgt_off:
            pwm_on = loop_time
            pwm_state = True
            GPIO.output(15,not pwm_state)
    if state is READY:
        if GPIO.input(11):
            sensor1 = loop_time
            state_change(SENSOR_2,loop_time)
    elif state is SENSOR_2:
#        if GPIO.input(12):
#            sensor2 = loop_time
#            GPIO.output(13,False)
#            state_change(RESET,loop_time)
        if not GPIO.input(11):
            sensor2 = loop_time
            state_change(CALCULATE,loop_time)	
    elif state is RESET_1:
        GPIO.setup(11,GPIO.OUT)
        GPIO.setup(12,GPIO.OUT)
        GPIO.output(11,False)
        GPIO.output(12,False)
        state_change(RESET_2,loop_time)
    elif state is RESET_2:
        GPIO.setup(11,GPIO.IN)
        GPIO.setup(12,GPIO.IN)
        GPIO.output(13,True)
        state_change(CALCULATE,loop_time)
    elif state is CALCULATE:
        print "Sensed interval:", sensor2-sensor1
        state_change(READY,loop_time)
    elif state is STARTUP:
        state_change(READY,loop_time)
        GPIO.output(15,False)

    print state.name,"\t\t",loop_time-state_time,"\tLoop Time",loop_time-last_loop,"\r",
    #loop_times.append(loop_time-last_loop)
    #print "Max Loop",max(loop_times),"\tMin loop",min(loop_times),"\tAvg Loop",sum(loop_times)/len(loop_times),"\r",
