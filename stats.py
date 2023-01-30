#

class text_object:
    def __init__(self, texts=[]):
        self.texts = texts

    def average_word_len(self): # Average Word length
        len_array = [];output = 0
        for line in texts:
            words = line.rstrip().split()
            for word in words:
                len_array.append(len(word))
        if len(len_array)>0:output = sum(len_array)/len(len_array)
        return output

    def average_sentence_len(self):# Average Sentence Length (counted in words)
        sentence_count = len(self.texts)
        sentence_len_array = [];output=0
        for line in texts:
            sentence_len_array.append(len(line))
        output = sum(sentence_len_array)/sentence_count
        return output
