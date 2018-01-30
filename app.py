from ghee.action import action_predict
from ghee.ner import ner_predict
from flask import Flask,request
import json
import sys
app = Flask(__name__)
app.config['SECRET_KEY'] = '22334455'


@app.route('/bulb',methods=['GET'])
def send_recieve():
   control = {'status':None, 'text':None, 'blue_state':0, 'red_state':0}
   if request.method=='GET':
      try:
         data = json.loads(request.data.decode('utf-8'))
         log(data)
      except (ValueError,TypeError,KeyError):
         print("Error caught")
         control['status'] = 0
         return json.dumps(control)
      control['status'] = 1
      data = request.args.get('text')
      intent = action_predict(str(data), 'bulb')
      ent = ner_predict(str(data),  'bulb')
      entities = []
      for i in ent:
          entities.append(i[1])
      log(entities)
      if intent == 'ON':
          control['text'] = "intent recognised ON \n"
          if 'blue' in entities:
              control['text'] = control['text']+'entity recognised Blue light \n'
              control['blue_state'] = 1
          elif 'red' in entities:
              control['text'] = control['text']+'entity recognised Red light \n'
              control['red_state'] = 1
          elif 'lights' in entities:
              control['text'] = control['text']+'entity recognised Blue light and Red light\n'
              control['red_state'] = 1
              control['blue_state'] = 1
      elif intent == 'OFF':
          control['text'] = "intent recognised OFF \n"
          if 'blue' in entities:
              control['text'] = control['text']+'entity recognised Blue light \n'
              control['blue_state'] = 0
          elif 'red' in entities:
              control['text'] = control['text']+'entity recognised Red light \n'
              control['red_state'] = 0
          elif 'lights' in entities:
              control['text'] = control['text']+'entity recognised Blue light and Blue light\n'
              control['red_state'] = 0
              control['blue_state'] = 0
      control = json.dumps(control)
      return control
def log(message):
    if message:
       print(str(message))
       sys.stdout.flush()
    else:
       print("NULL")
       sys.stdout.flush()
#port_=int(sys.argv[1])

if __name__ == '__main__':
    app.debug = True
    app.run()