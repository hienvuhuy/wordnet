# -*- coding: utf-8 -*-
import re
import nltk
import myWordnet
from myWordnet import WordNetCorpusReader
from Constant.py import Constant

class VietnameseSynset:
    def __init__(self):
        self._name = None
        self._english = None
        self._gloss  = None
        self._examples = []
        self._synonyms = []
        self._frame_ids = []
        self._hypernyms = []
    def name(self):
        return self._name
    def english(self):
        return self._english
    def gloss(self):
        return self._gloss
    def examples(self):
        return self._examples
    def synonyms(self):
        return self._synonyms
    def frame_ids(self):
        return self._frame_ids
    def hypernyms(self):
        return self._hypernyms
    def setFrames(self, frame_ids):
        for frame in frame_ids:
            self._frame_ids.append(frame)
    def setHypernyms(self, hypernyms):
        for hypernym in hypernyms:
            self._hypernyms.append(hypernym)
    def set_synset_from_line(self, line):
        line = line.strip()
        line_entries = re.split(r'\t+', line)
        # the line are ignored if it have no vietnamese meaning
#         if line_entries[3].strip() == '[]': 
        # set english word that correspond with vietnamese word
        self._english = line_entries[0].strip().translate(None, remove_symbol)
        
        # get definition
        self._gloss = line_entries[1].strip().translate(None, remove_symbol)
        
        #get examples
        examples = line_entries[2].strip().translate(None, remove_symbol)
        if len(examples) > 0:
            example_entries = examples.split(',')
            index_emxample = 0
            number_of_examples = len(example_entries)
            while index_emxample < number_of_examples:
                example = example_entries[index_emxample].strip()
                self._examples.append(example)
                index_emxample += 1
            
        # get synonyms
        synonyms = line_entries[3].strip().translate(None, remove_symbol)
        vietnamese_words = synonyms.split(',')
        # insert underscore symbol
        word_sense = insert_underscore_symbol(vietnamese_words[0].strip())
        # generate lex_id 
        self._name = generate_lex_id(word_sense)
        index_synnonym = 1
        number_of_synonym = len(vietnamese_words)
        while index_synnonym < number_of_synonym:
            word = vietnamese_words[index_synnonym].strip()
            synset = insert_underscore_symbol(word)
            synset = generate_lex_id(synset)
            self._synonyms.append(synset)
            index_synnonym += 1

def removeComments(string):
    # remove all occurance singleline comments (//COMMENT\n) from string
    string = re.sub(re.compile("//.*?\n"),"" ,string)
    return string

# insert underscore symbol into collocation
def insert_underscore_symbol(collocation):
    str_underscore = '_'
    collo_parts = collocation.strip().split(' ')
    return str_underscore.join(collo_parts)

def load_data(resource_name, start_file):
    resource = open(resource_name, 'rb')
    data = resource.readlines()[start_file:]
    resource.close()
    return data

# load data into a hash that has keys are English words and values are vietnamese synsets corresponding
def load_data_to_hash(resource_name, start_file, hash):
    data = load_data(resource_name, start_file)
    i = 1
    leng_of_data = len(data)
    while i < leng_of_data:
        if not (data[i].startswith(comment_symbol1) or data[i].startswith(need_check_symbol)):
            print("%s %s" %(i, data[i]))
            vi = VietnameseSynset()
            vi.set_synset_from_line(data[i])
            key = vi.english()
            value = vi
            hash[key] = value
        if (i+1) < leng_of_data and data[i+1].startswith(comment_symbol1):
            i += 3
        else:
            i += 2
# return lex_id that is a sense number of a word           
def generate_lex_id(synset_name):
    if hash_lex_id.get(synset_name) == None:
        hash_lex_id[synset_name] = 0;
    else:
        hash_lex_id[synset_name] = hash_lex_id.get(synset_name) + 1
    lex_id = hash_lex_id[synset_name]
    if lex_id == 0:
        return synset_name
    else:
        return synset_name + str(lex_id)

def print_synsets(synset):
    str_line = "{ "
    str_line += synset.name() + ", "
    for synonym in synset.synonyms():
        str_line += synonym + ", "
    for hypernym in synset.hypernyms():
        str_line += hypernym + ",@ "
        
    frames = synset.frame_ids()
    number_of_frames = len(frames)
    if number_of_frames != 0:
        str_line += "frames: "
        comma_symbol = ","
        str_line += comma_symbol.join(map(str, frames))
        str_line += " "
        
    if synset.gloss() != None:
        str_line += "(" + synset.gloss()
        
    examples = synset.examples()
    number_of_example = len(examples)
    if number_of_example != 0:
        for example in examples:
            str_line += '; "' + example + '"'
    str_line += ') }'
    return str_line

# source_path = "/home/thuannm/VietLexicographer/data_verb/2015-03-23.fileouttype.verb.body.chang.txt"
# destination_path = "/home/thuannm/VietLexicographer/verb.body"

# source_path = "/home/thuannm/VietLexicographer/data_verb/2015-03-23.fileouttype.verb.creation.chang.txt"
# destination_path = "/home/thuannm/VietLexicographer/verb.creation"

source_path = Constant.source_verb_social_path
destination_path = Constant.destination_verb_social_path

comment_symbol1 = "//"
need_check_symbol = "***"
comment_symbol2 = "////"
remove_symbol = "\'[]*"

# open file to write
file_destination = open(destination_path, 'w')
# hash to store data with keys are english words and values are vietnamese words corresponding
hash_mapping = {}
start_file = 8
# hash to generate sense number of a word
hash_lex_id = {} 

print('loading data into hash')
load_data_to_hash(source_path, start_file, hash_mapping)
print('done loading')
  
print('loading wordnet')
wn = WordNetCorpusReader(nltk.data.find('corpora/wordnet'), None)
print('done loading')
S = wn.synset 

# search hypernym and frame_ids of synset in wordnet
for key, value in hash_mapping.iteritems():
    print (hash_mapping[key].gloss())
    synset = S(key)
    # add frame_ids
    value.setFrames(synset.frame_ids())
    
    if len(synset.hypernyms()) == 0:
        print(key," no hypernym")
    # search hypernym
    for hypernym in synset.hypernyms():
        key_hypernym = hypernym.name()
        value_hypernym = hash_mapping.get(key_hypernym)
        if value_hypernym != None:
            value._hypernyms.append(value_hypernym.name())
    line = print_synsets(value)
#     print(line)
    file_destination.write(line + "\n")

hash_mapping.clear()
hash_lex_id.clear()
