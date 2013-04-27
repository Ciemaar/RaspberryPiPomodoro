__author__ = 'andriod'

import plivo


auth_id = "MANTY3OWMWOWYWNDNHY2"
auth_token = "MGY2ZmQ5NTY0Yjk1MjQ1MzZmZmUyY2YyZWMwM2Ew"

p = plivo.RestAPI(auth_id, auth_token)

# Send a SMS
params = {
    'src': '12021234567890', # Caller Id
    'dst' : '14242436227', # User Number to Call
    'text' : "Hi, message from Plivo",
    'type' : "sms",
    }

#p.send_message(params)


#params = {'from':"14242436227",'to':'14242436227','answer_url':"http://ciemaar.pythonanywhere.com/static/call_mom/answer.xml",'answer_method':"GET"}
params = {'from':"14242436227",'to':'12019932664','answer_url':"http://ciemaar.pythonanywhere.com/static/call_mom/answer.xml",'answer_method':"GET"}

response = p.make_call(params)
print response
