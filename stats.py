import math

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
        for line in texts:
            sentence_len_array.append(len(line.split()))
        output = sum(sentence_len_array)/sentence_count
        return output

    def average_sentence_chr_len(self):# Average Sentence Length (counted in characters)
        sentence_count = len(self.texts)
        sentence_len_array = [];output=0
        for line in texts:
            sentence_len_array.append(len(line))
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
        compound_words = [i for i in len_array if (len(i)>=30)]
        if (len(len_array)>0):output = len(compound_words)/len(len_array)
        return output

    def word_len_distribution(self):
        this_dict = {};len_array=self.get_word_len()
        for i in len_array:
            this_dict[i] = this_dict.get(i,0) + 1
        return this_dict
        
    
