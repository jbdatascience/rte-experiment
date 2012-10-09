#!/usr/bin/python
#
# Bismillahi-r-Rahmani-r-Rahim
# Create an RTE dataset

import os
#import nltk
#from nltk.tokenize import sent_tokenizer
from nltk import word_tokenize, tokenize
from nltk.tag import pos_tag
from entailment.NGramOverlap import NGramOverlap
#from save_dataset import save
from db import RteDb
import nltk

data_dir = '/home/daoud/Data/rte'

output_path = '../output/'

pos_threshold = 0.578
neg_threshold = 0.4
rte = NGramOverlap(3, pos_threshold)
#max_pairs = 200000
max_pairs = 10

ne_tagger = nltk.data.load('chunkers/maxent_ne_chunker/english_ace_binary.pickle')

def valid_sentence(text):
    if len(text) < 30:
        return False
    if len(text) > 500:
        return False
    if text.count('"') % 2 != 0:
        return False
    if text.count('\n') > 4:
        return False
    return True

def ent(text, hypothesis):
    global rte
    if not valid_sentence(text) or not valid_sentence(hypothesis):
        return False
    return rte.ent( (text, hypothesis) )

def output_pairs(positive, negative):
    if len(negative) > len(positive):
        negative.sort()
        negative.reverse()
        negative = negative[:len(positive)]
        negative = [x[1:3] for x in negative]
        #print negative
    else:
        print "Warning: more positive than negative."

    print "Positive:", len(positive)
    print "Negative:", len(negative)
    save(positive, negative, os.path.join(output_path, 'dataset.xml'))

def get_entities(sentence):
    tags = pos_tag(word_tokenize(sentence))
    parse = ne_tagger.parse(tags)
    entities = set([x[0] for x in parse.pos() if x[-1] == 'NE'])
    #entities = [list(x) for x in parse if type(x) == nltk.tree.Tree and x.pos()[0][-1] == 'NE']
    return entities

def process_documents(path):
    positive_pairs = []
    negative_pairs = []
    
    subdirs = os.listdir(path)
    subdirs.sort()
    #headlines = []
    for s in subdirs:
        new_path = os.path.join(path,s)
        files = os.listdir(new_path)
        files.sort()
        for f in files:
            file_path = os.path.join(new_path,f)
            print file_path
            file_ = open(file_path)
            headline = file_.readline()[:-1]
            body = file_.read()
            sentences = tokenize.sent_tokenize(body)
            if ent(sentences[0], headline) > pos_threshold:
                print sentences[0]
                print headline
                print
                positive_pairs.append( (sentences[0], headline) )
            if len(positive_pairs) < len(negative_pairs):
                continue
            for i in range(1, len(sentences) - 1):
                text = sentences[i]
                hypothesis = sentences[i + 1]
                entities1 = get_entities(text)
                entities2 = get_entities(hypothesis)
                if len(entities1 & entities2) > 0:
                    print "-- Non entailing --"
                    print text
                    print hypothesis
                    negative_pairs.append( (0, text, hypothesis) )
                    if len(positive_pairs) < len(negative_pairs):
                        break
                    
                    
            # for sentence in sentences[1:]:
            #     for i in range(len(headlines)):
            #         text = sentence
            #         hypothesis = headlines[i]
            #         val = ent(text, hypothesis)
            #     # text = headline #sentences[i]
            #     # hypothesis = sentence
            #     # val = ent(text, hypothesis)
            #         if val > pos_threshold:
            #             print "-- Non entailing --"
            #             print text
            #             print hypothesis
            #             print
            #             negative_pairs.append( (val, text, hypothesis) )
            #             del headlines[i]
            #             break
            #if (valid_sentence(headline)):
            #    headlines.append(headline)
            if len(positive_pairs) >= max_pairs and len(negative_pairs) >= max_pairs:
                output_pairs(positive_pairs, negative_pairs)
                return
    output_pairs(positive_pairs, negative_pairs)

if __name__ == "__main__":
    global data_dir
    process_documents(data_dir)
