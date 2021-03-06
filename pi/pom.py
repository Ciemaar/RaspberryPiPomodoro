import time
import RPi.GPIO as GPIO
from toodledo import get_pom_tasks,config, taskRegex, save_current_config, update_task_numbers, client
import os

try:
    rows, columns = os.popen('stty size', 'r').read().split()
    rows = int(rows)
except ValueError:
    rows = 56

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(12, GPIO.IN)
GPIO.setup(16, GPIO.IN)
GPIO.setup(18, GPIO.IN)
GPIO.setup(22, GPIO.IN)

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
update_time = 0
display_time = 0
pom_time = 0
pom_tasks = []

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
    #print "\n",state.name,"->",new_state.name,"\n"
    if state is POM and new_state is BREAK and currentTask is not None: # normal end of POM
        client.editTask(currentTask.id, note = "Completed a POM")
    state = new_state
    button_time = time.time() + 3 * LONG_PUSH

if not config.has_section('cache'):
    config.add_section('cache')

while True:
    pushed = 0
    if button_time:
        pushed = time.time() - button_time
        if GPIO.input(12):
            button_time = None
            if pushed < SHORT_PUSH:
                pushed = 0
        elif pushed < LONG_PUSH:
                pushed = 0
    elif not GPIO.input(12):
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
      GPIO.output(11, led_curr)

    if time.time() > pom_time + 60: # Rate limit 2 calls per minute
        try:
            currentTaskNo = str((1-GPIO.input(16))+ 2 * (1-GPIO.input(18))+ 4 *(1-GPIO.input(22)))
            currentTask = None

            pom_tasks = get_pom_tasks()
            pom_time = time.time()
            for task in pom_tasks:
                extract = taskRegex.match(task.title)
                if extract:
                   taskNo = extract.group(1)
                   if taskNo == currentTaskNo:
                       currentTask = task
                config.set("cache","task"+taskNo,task.title)
            config.set("cache","pom_time",str(pom_time))
            save_current_config()
        except:
            pass

    if time.time() > display_time + 15: # refresh every 15 seconds
        print "\n"*(rows-(3+len(pom_tasks)))
        for task in pom_tasks:
            print task.title, task.duedate
        print "Currently:",currentTaskNo
        if currentTask is not None:
            print currentTask.title
        else:
            print "No Task\n"
        display_time = time.time()

    if time.time() > update_time + 600: # update task numbers every 10 minutes
        update_task_numbers()
        update_time = time.time()