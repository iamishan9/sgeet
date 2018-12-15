

from pprint import pprint
import nltk
import yaml
#import sys
#import os
#import re
#import json
#import ast


count_happy=0
count_sad=0
count_relax=0
count_romantic=0
class Splitter(object):

    def __init__(self):
        self.nltk_splitter = nltk.data.load('tokenizers/punkt/english.pickle')
        self.nltk_tokenizer = nltk.tokenize.TreebankWordTokenizer()

    def split(self, text):

        sentences = self.nltk_splitter.tokenize(text)
        tokenized_sentences = [self.nltk_tokenizer.tokenize(sent) for sent in sentences]
        return tokenized_sentences


class POSTagger(object):

    def __init__(self):
        pass
        
    def pos_tag(self, sentences):


        pos = [nltk.pos_tag(sentence) for sentence in sentences]
        #adapt format
        pos = [[(word, word, [postag]) for (word, postag) in sentence] for sentence in pos]
        return pos

class DictionaryTagger(object):

    def __init__(self, dictionary_paths):
        files = [open(path, 'r') for path in dictionary_paths]
        dictionaries = [yaml.load(dict_file) for dict_file in files]
        map(lambda x: x.close(), files)
        self.dictionary = {}
        self.max_key_size = 0
        for curr_dict in dictionaries:
            for key in curr_dict:
                if key in self.dictionary:
                    self.dictionary[key].extend(curr_dict[key])
                else:
                    self.dictionary[key] = curr_dict[key]
                    self.max_key_size = max(self.max_key_size, len(key))

    def tag(self, postagged_sentences):
        return [self.tag_sentence(sentence) for sentence in postagged_sentences]

    def tag_sentence(self, sentence, tag_with_lemmas=False):

        tag_sentence = []
        N = len(sentence)
        if self.max_key_size == 0:
            self.max_key_size = N
        i = 0
        while (i < N):
            j = min(i + self.max_key_size, N) #avoid overflow
            tagged = False
            while (j > i):
                expression_form = ' '.join([word[0] for word in sentence[i:j]]).lower()
                expression_lemma = ' '.join([word[1] for word in sentence[i:j]]).lower()
                if tag_with_lemmas:
                    literal = expression_lemma
                else:
                    literal = expression_form
                if literal in self.dictionary:
                    #self.logger.debug("found: %s" % literal)
                    is_single_token = j - i == 1
                    original_position = i
                    i = j
                  
                    taggings = [tag for tag in self.dictionary[literal]]
                    
                    tagged_expression = (expression_form, expression_lemma, taggings)
                    if is_single_token: #if the tagged literal is a single token, conserve its previous taggings:
                        original_token_tagging = sentence[original_position][2]
                        tagged_expression[2].extend(original_token_tagging)
                    tag_sentence.append(tagged_expression)
              
                    tagged = True
                else:
                    j = j - 1
            if not tagged:
                tag_sentence.append(sentence[i])
                i += 1
        return tag_sentence

def value_of(sentiment):
 
   
    
    if sentiment=='happy':return 'happy'

    elif sentiment=='sad': return 'sad'

    elif sentiment == 'relax':return 'relax'
    elif sentiment=='romantic': return 'romantic'
    

    


def sentence_score(sentence_tokens, previous_token):    
    global count_happy
    global count_sad
    global count_relax
    global count_romantic
    token_value=1
    if not sentence_tokens:
        return 0.0
    else:
        current_token = sentence_tokens[0]
        tags = current_token[2]
        token_score = [value_of(tag) for tag in tags]
       # pprint(token_score[0])
             
        if previous_token is not None:
            previous_tags = previous_token[2]
            if 'inc' in previous_tags:
                token_value *= 2.0
            elif 'dec' in previous_tags:
                token_value /= 2.0
            elif 'inv' in previous_tags:
                token_value *= -1.0
        
    if token_score[0]=='happy':
        count_happy+=1
        count_happy=token_value
    if token_score[0]=='sad':
        count_sad+=1
        count_sad=token_value
    if token_score[0]=='relax':
        count_relax+=1
        count_relax=token_value
    if token_score[0]=='romantic':
        count_romantic+=1
        count_romantic=token_value
        
        
    return sentence_score(sentence_tokens[1:], current_token)

def sentiment_score(review):
  return [sentence_score(sentence, None) for sentence in review]

if __name__ == "__main__":
    text =open("fbdump.csv").read()

    splitter = Splitter()
    postagger = POSTagger()
    dicttagger = DictionaryTagger([ 'dicts/sad.yml', 'dicts/romantic.yml',
                                    'dicts/inc.yml', 'dicts/dec.yml', 'dicts/inv.yml', 'dicts/happy.yml', 'dicts/relax.yml' ])

    splitted_sentences = splitter.split(text)
    pprint(splitted_sentences)

    pos_tagged_sentences = postagger.pos_tag(splitted_sentences)
    pprint(pos_tagged_sentences)

    dict_tagged_sentences = dicttagger.tag(pos_tagged_sentences)
    pprint(dict_tagged_sentences)


    print("analyzing sentiment...")
    score = sentiment_score(dict_tagged_sentences)
    #print(score)

    print(count_sad)
    print(count_relax)
    print(count_happy)
    print(count_romantic)
    if count_happy > count_sad and count_happy>count_relax and count_happy>count_romantic:
        print("Happy")
        outfile=open("output.txt","w")
        outfile.write("happy")
    elif count_sad> count_relax and count_sad>count_happy and count_sad>count_romantic:
        print("Sad")
        outfile = open("output.txt", "w")
        outfile.write("sad")
    elif count_relax > count_sad and count_relax > count_happy and count_relax>count_romantic:
        print("Relax")
        outfile = open("output.txt", "w")
        outfile.write("relax")
    elif count_romantic>count_sad and count_romantic>count_happy and count_romantic>count_relax:
        print("Romantic")
        outfile = open("output.txt", "w")
        outfile.write("romance")
    else :
        print("Neutral")
        outfile = open("output.txt", "w")
        outfile.write("neutral")


