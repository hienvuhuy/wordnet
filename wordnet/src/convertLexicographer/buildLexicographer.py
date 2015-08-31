# -*- coding: utf-8 -*-
import re
import nltk


class VietnameseSynset:
    def __init__(self):
        
        self._name = None
        self._english = None
        self._gloss  = None
        self._examples = []
        self._synonyms = []
        self._frame_ids = []
        
        self._antonym = []
        self._hypernyms = []
        self._instanceHypernym = []
        self._hyponym = []
        self._instanceHyponym = []
        self._memberHolonym = []
        self._partHolonym = []
        self._memberMeronym = []
        self._substanceMeronym = []
        self._partMeronym = []
        self._attribute = []
        
        #verb
        self._entailment = []
        self._cause = []
        self._alsoSee = []
        self._verbGroup = []
        
        #adj
        self._similarTo = []
        self._participleOfVerb =[]
        self._pertainym = []
        
        
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