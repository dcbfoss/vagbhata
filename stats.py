import math
import gl
class text_object:
    def __init__(self, texts=[]):
        self.texts = texts

    def get_word_len(self):
        len_array = []
        for line in self.texts:
            words = line.rstrip().split()
            for word in words:
                len_array.append(len(word))
        return len_array

    def average_word_len(self): # Average Word length
        output = 0;len_array=self.get_word_len()
        if len(len_array)>0:output = sum(len_array)/len(len_array)
        return output

    def average_sentence_word_len(self):# Average Sentence Length (counted in words)
        sentence_count = len(self.texts)
        sentence_len_array = [];output=0
        for line in self.texts:
            sentence_len_array.append(len(line.split()))
        output = sum(sentence_len_array)/sentence_count
        return output

    def average_sentence_chr_len(self):# Average Sentence Length (counted in characters)
        sentence_count = len(self.texts)
        sentence_len_array = [];output=0
        for line in self.texts:
            syl = gl.get_syllables(line.rstrip())
            sentence_len_array.append(len(syl))
        output = sum(sentence_len_array)/sentence_count
        return output

    
    def get_richness_ratio(self): # get richness ratio
        total_words = 0
        words_collection = {}
        for line in self.texts:
            words = line.rstrip().split(" ")
            total_words += len(words)
            for word in words:
                words_collection[word] = words_collection.get(word,0) + 1
        return len(words_collection.keys())/total_words

    
    def get_richness_of_words(self): # richness of each words for shannon
        total_words = 0
        words_collection = {}
        for line in self.texts:
            words = line.rstrip().split(" ")
            total_words += len(words)
            for word in words:
                words_collection[word] = words_collection.get(word,0) + 1
        for word in words_collection.keys():
            words_collection[word] = words_collection[word]/total_words
        return words_collection

    
    def get_shannon(self): # shannon entropy
        output = 0
        richness = self.get_richness_of_words()
        for entry in richness.keys():
            output = output + richness[entry]/math.log(richness[entry],2)
        return -1 * output

    def average_compound_words(self):
        output = 0;len_array=self.get_word_len()
        compound_words = [i for i in len_array if (i >= 30)]
        if (len(len_array)>0):output = len(compound_words)/len(len_array)
        return output

    def word_len_distribution(self):
        this_dict = {};len_array=self.get_word_len()
        for i in len_array:
            this_dict[i] = this_dict.get(i,0) + 1
        return this_dict

def crop_by_three(text):
    output = []
    while len(text)>0:
        output.append(text[0:3])
        text = text[3:]
    return output

def chi_square(block1, block2):
    b1_lg = [crop_by_three(''.join(gl.get_lg(gl.get_syllables(i))).replace('-','')) for i in block1]
    b2_lg = [crop_by_three(''.join(gl.get_lg(gl.get_syllables(i))).replace('-','')) for i in block2]
    merged = []; b1_lg_arr = []; b2_lg_arr = [];output = 0
    for i, j in zip(b1_lg, b2_lg):
        for k, l in zip(i, j):
            if not(k in merged):merged.append(k)
            if not(l in merged):merged.append(l)
    b1_lg_arr = [0 for i in merged]
    b2_lg_arr = [0 for i in merged]
    for i, j in zip(b1_lg, b2_lg):
        for k, l in zip(i, j):
            b1_lg_arr[merged.index(k)] += 1
            b2_lg_arr[merged.index(l)] += 1
    b1_sum = sum(b1_lg_arr); b2_sum = sum(b2_lg_arr); count_b1_b2 = b1_sum + b2_sum
    for i in range(len(b1_lg_arr)):
        this_sum = b1_lg_arr[i]+b2_lg_arr[i]
        this_b1_val = ((this_sum * b1_sum) / count_b1_b2)
        this_b2_val = ((this_sum * b1_sum) / count_b1_b2)
        output = output + (((b1_lg_arr[i]-this_b1_val)**2)/this_b1_val) + (((b1_lg_arr[i]-this_b2_val)**2)/this_b2_val)
    return output
    
