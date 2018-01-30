
import numpy as np
import random

def dataclean(training_data):

    all_categories = list()  # list to store categories of intent
    all_words = list()  # for storing all words to convert input sentence into bag of words
    for data in training_data:
        if data["intent"] not in all_categories:
            all_categories.append(data["intent"])
        for word in data["sentence"].split(" "):
            #  storing words in each sentence
            if word not in all_words:
                all_words.append(word)
    return all_categories, all_words

def wordToIndex(word,all_words):
    # finding indx of a word from all_words
    return all_words.index(word)


def sentencetotensor(sentence,all_words):
    # input tensor initialized with zeros
    n_words = len(all_words)
    tensor = np.zeros(n_words)
    for word in sentence.split(" "):
        if word not in all_words:
            # to deal with words not in dataset in evaluation stage
            continue
        tensor[wordToIndex(word, all_words)] = 1  # making found word's position 1
    return tensor


def randomchoice(length):
    # random function for shuffling dataset
    return length[random.randint(0, len(length)-1)]


def randomtrainingexample(training_data,all_categories,all_words):
    # produce random training data
    training = []
    #output = []
    output = np.zeros((len(training_data),len(all_categories)))
    for k in range(len(training_data)):

        data = training_data[k]
        category = data['intent']
        output[k][all_categories.index(category)] = 1
        #category_tensor = np.array([all_categories.index(category)])
        # creating target Tensor
        sentence = data["sentence"]  # input
        line_tensor = np.array(sentencetotensor(sentence, all_words))  # input tensor
        training.append(line_tensor)
        #output.append(category_tensor)
    return sentence, output, np.array(training)