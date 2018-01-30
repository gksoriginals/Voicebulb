from ghee.ner import ner_predict
from ghee.action import action_predict
print(ner_predict('turn on all lights', 'bulb'))
print(action_predict('turn off lights', 'bulb'))
