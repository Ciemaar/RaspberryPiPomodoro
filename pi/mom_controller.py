from time import sleep

try:
    import RPi.GPIO as GPIO
except ImportError:
    import RPiFake.GPIO as GPIO

import time
from collections import deque

import plivo

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN)
GPIO.setup(11, GPIO.IN)
GPIO.setup(13, GPIO.IN)
GPIO.setup(15, GPIO.IN)


auth_id = "MANTY3OWMWOWYWNDNHY2"
auth_token = "MGY2ZmQ5NTY0Yjk1MjQ1MzZmZmUyY2YyZWMwM2Ew"

p = plivo.RestAPI(auth_id, auth_token)
while True:
    if GPIO.input(7):
        #Call Mom
        params = {'from':"14242436227",'to':'12019932664','answer_url':"http://ciemaar.pythonanywhere.com/static/call_mom/answerThenCallMom.xml",'answer_method':"GET"}
        p.make_call(params)
    elif  GPIO.input(11):
        #CallDad
        params = {'from':"14242436227",'to':'12019932664','answer_url':"http://ciemaar.pythonanywhere.com/static/call_mom/answerThenCallYou.xml",'answer_method':"GET"}
        p.make_call(params)
    elif  GPIO.input(13):
        params = {
            'src': '12019932664', # Caller Id
            'dst' : '14242436227', # User Number to Call
            'text' : "Hi, message from Plivo",
            'type' : "sms",
            }

        p.send_message(params)
    elif  GPIO.input(15):
        pass
    sleep(.1)