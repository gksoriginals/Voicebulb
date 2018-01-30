import random
import json
import os
import pickle
import numpy as np
from ghee.nn import ANN
from ghee.dataprocess import dataclean, randomtrainingexample, sentencetotensor

def action_train(training_data, num_iter, bot_loc):
    """function for training the intent recogniser"""
    all_categories, all_words = dataclean(training_data)
    #print(all_categories)
    output_size = len(all_categories)
    hidden_size = 128
    sentence, output, input_ = randomtrainingexample(training_data, all_categories, all_words)
    input_size = len(input_[0])
    neuralnet = ANN(input_size, output_size,hidden_size, alpha=0.005)
    neuralnet.run(input_, output, num_iter)
    if not os.path.exists(bot_loc+'/brain'):
        os.makedirs(bot_loc+'/brain')
    file_ = open(os.path.join(bot_loc+'/brain', 'neuralpkl.pkl'),'wb')
    pickle.dump(neuralnet,file_)
    file_ = open(os.path.join(bot_loc+'/brain','meta.pkl'), 'wb')
    pickle.dump([all_categories, all_words], file_)
def action_predict(sentence, bot_loc):
    """function for predicting the action"""
    with open(os.path.join(bot_loc+'/brain','neuralpkl.pkl'),'rb') as file_:
         neuralnet = pickle.load(file_)
    with open(os.path.join(bot_loc+'/brain','meta.pkl'), 'rb') as file_:
         meta = pickle.load(file_)
         all_categories = meta[0]
         all_words = meta[1]
    line_tensor = np.array(sentencetotensor(sentence, all_words))
    k, value = neuralnet.evaluate(line_tensor)
    if value > 0.8:
       return all_categories[k]
    else:
        return "none"