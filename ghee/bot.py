import os
import json
import random
import pickle
import datetime
from ghee.action import action_train, action_predict

class create_bot():
    def __init__(self, bot_name, dsl):
        self.botname = bot_name
        self.dsl = dsl
        with open('ghee/datasets/action_dataset.json') as data_file:
            data = json.load(data_file)
        if not os.path.exists(self.botname+'/datasets'):
            os.makedirs(self.botname+'/datasets')
        with open(os.path.join(self.botname+'/datasets', 'action_dataset.json'),'w', encoding='utf8') as data_file:
            json.dump(data, data_file)
    def run_bot(self, sentence):
        """function to run the bot"""
        intent = action_predict(str(sentence), self.botname)
        reply = self.dsl(intent, sentence)
        if reply == "none":
           reply = random.choice(["there must be an error", "ask that gopi to fix me :(", "sorry this is a prototype"])
        return reply
    def action_train_protocol(self, sentence, Train=True):
        """function to train the action prediction model"""
        if Train:
           training_data = []
           with open(self.botname+'/datasets/action_dataset.json') as data_file:
                data = json.load(data_file)

           for line in data:
               #fetching training data
               training_data.append(line)
           action_train(training_data, 20000, self.botname) #training the model
        print("intent:" + action_predict(sentence, self.botname))
    def test_run_protocol(self):
        """function for test running the bot"""
        while True:
           k = input("user: ")
           print(self.botname+": ", self.run_bot(k))

