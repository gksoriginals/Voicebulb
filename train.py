import json
from ghee.action import action_train, action_predict
from ghee.ner import ner_train, ner_predict
def action_train_protocol(sentence, Train=True):
    """function to train the action prediction model"""
    if Train:
        training_data = []
        with open('datasets/action_dataset.json') as data_file:
            data = json.load(data_file)

        for line in data:
             #fetching training data
             training_data.append(line)
        action_train(training_data, 20000, 'bulb')
        print(action_predict(sentence, 'bulb'))
def ner_train_protocol(sentence):
    tdata = [
    ('turn on lights', [('lights', 'bulb')]),('turn off lights', [('lights', 'bulb')]),('turn on blue light',[('blue', 'bulb')]),('turn off blue light', [('blue', 'bulb')]),('turn on blue light and red light', [('blue', 'bulb'), ('red', 'bulb')]), ('turn off both lights', [('lights', 'bulb')])]
    ner_train(tdata, output_dir='bulb')
    print(ner_predict(sentence, 'bulb'))
action_train_protocol('turn on violet light')
ner_train_protocol('turn off red light and blue light')
