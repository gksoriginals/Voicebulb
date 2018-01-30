import os.path
from ghee.action import action_predict
from ghee.ner import ner_predict
from flask import Flask,request,Response
import json
import sys
app = Flask(__name__)
app.config['SECRET_KEY'] = '22334455'

def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))

def get_file(filename):  # pragma: no cover
    try:
        src = os.path.join(root_dir(), filename)
        return open(src).read()
    except IOError as exc:
        return str(exc)

@app.route('/',methods=['GET'])
def fun1():
    content = get_file('html/index.html')
    return Response(content, mimetype="text/html")

@app.route('/index.js',methods=['GET'])
def fun2():
    content = get_file('html/index.js')
    return Response(content, mimetype="text/javascript")

@app.route('/index.css',methods=['GET'])
def fun3():
    content = get_file('html/index.css')
    return Response(content, mimetype="text/css")

@app.route('/bulb',methods=['GET'])
def send_recieve():
   control = {'status':None, 'text':None, 'blue_state':0, 'red_state':0}
   if request.method=='GET':
      control['status'] = 1
      data = request.args.get('text')
      intent = action_predict(str(data), 'bulb')
      ent = ner_predict(str(data),  'bulb')
      entities = []
      for i in ent:
          entities.append(i[1])
      log(entities)
      arr = []
      if intent == 'ON':
          arr.append("Intent recognised : ON")
          if 'blue' in entities:
              arr.append("Entity recognised : Blue light")
              control['blue_state'] = 1
          elif 'red' in entities:
              arr.append("Entity recognised : Red light")
              control['red_state'] = 1
          elif 'lights' in entities:
              arr.append("Entity recognised : Blue light and Red light")
              control['red_state'] = 1
              control['blue_state'] = 1
      elif intent == 'OFF':
          arr.append("Intent recognised : OFF")
          if 'blue' in entities:
              arr.append("Entity recognised : Blue light")
              control['blue_state'] = 2
          elif 'red' in entities:
              arr.append("Entity recognised : Red light")
              control['red_state'] = 2
          elif 'lights' in entities:
              arr.append("Entity recognised : Lights")
              control['red_state'] = 2
              control['blue_state'] = 2
      control["text"] = arr
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
