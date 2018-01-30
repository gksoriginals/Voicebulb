from __future__ import unicode_literals, print_function
import os
import random
from pathlib import Path
import spacy



tdata = [
    ('I am going to vaikom by bus.', [('vaikom', 'LOC'), ('bus', 'VEH')]),
('I like london.', [('london', 'LOC')]),
('I am going to berlin by train.',[('berlin', 'LOC'), ('train', 'VEH')]),
('I like vaikom.', [('vaikom', 'LOC')])
]



def ner_train(training_data, model=None, output_dir=None, n_iter=20):
    """Set up the pipeline and entity recognizer, and train the new entity."""
    TRAIN_DATA = []
    if model is not None:
        nlp = spacy.load(model)
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank('en')
        print("Created blank 'en' model")


    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner)
    # otherwise, get it, so we can add labels to it
    else:
        ner = nlp.get_pipe('ner')


    labels = []
    entities = []
    k = dict()
    for data in training_data:
        sent = data[0]
        annot = data[1]
        for tuple in annot:
            if tuple[1] not in labels:
                labels.append(tuple[1])
            start = sent.find(tuple[0])
            end  = start+len(tuple[0])
            if start!=-1:
                entities.append((start, end, tuple[1]))
        k["entities"] = entities
        entities = []
        TRAIN_DATA.append((sent, k))
        k = dict()
    print(TRAIN_DATA)
    for i in labels:
        ner.add_label(i)
    new_model_name = output_dir
    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):  # only train NER
        optimizer = nlp.begin_training()
        for itn in range(n_iter):
            random.shuffle(TRAIN_DATA)
            losses = {}
            for text, annotations in TRAIN_DATA:
                nlp.update([text], [annotations], sgd=optimizer, drop=0.35,
                           losses=losses)
            print(losses)



    # save model to output directory
    if output_dir is not None:
        #output_dir = Path(output_dir)
        if not os.path.exists(output_dir+'/brain'):
            os.makedirs(output_dir+'/brain')
        nlp.meta['name'] = new_model_name  # rename model
        nlp.to_disk(output_dir+'/brain')
        print("Saved model to", output_dir+'/brain')

        # test the saved model
        # test the trained model
def ner_predict(sentence, output_dir):
    #print("Loading from", output_dir)
    out = []
    #output_dir = Path(output_dir)
    nlp2 = spacy.load(output_dir+'/brain')
    doc2 = nlp2(sentence)
    for ent in doc2.ents:
        out.append((ent.label_, ent.text))
    return out



