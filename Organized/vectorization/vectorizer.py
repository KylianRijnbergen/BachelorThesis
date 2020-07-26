from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pandas as pd
import csv
import warnings
warnings.filterwarnings("ignore")

GLOVE_DIRECTORY = "C:/Users/Kylian Rijnbergen/Documents/TBK/Year_3/Module 12/"
words = pd.read_table(
        GLOVE_DIRECTORY + "glove.840B.300d.txt", 
        sep=" ", 
        index_col=0, 
        header=None, 
        quoting=csv.QUOTE_NONE
        )

MEMOIZE = True
#function for getting the vector of a word. Uses Memoization.

vec_cache = {}
def vec(w):
    if w in vec_cache:
        return vec_cache[w]
    try:
        word_vector = words.loc[w].as_matrix()
        if MEMOIZE:
            vec_cache[w] = word_vector
        return word_vector
    except:
        pass
       

#Definition of class BagOfWords
class BagOfWords:
    """
    BagOfWords converts a string to a bag of words. Attributes: matrix, tokens
    """
    
    def __init__(self, string):
        vectorizer = CountVectorizer()
        self.words_one_hot = vectorizer.fit_transform(string.split(" ")).toarray()
        self.tokens = vectorizer.get_feature_names()

#Definition of class Vectorize.
class Vectorize:
    """ 
    This class vectorizes strings.
    """
    
    def __init__(self, string):
        self.string = str(string)
        words_one_hot = BagOfWords(self.string).words_one_hot
        self.word_counts = np.sum(words_one_hot, axis = 0)
        self.tokens = BagOfWords(self.string).tokens
        self.all_vectors = np.empty([0,301])
        self.vectorize()
        self.get_weighted_average_vector()
        return
                
    def vectorize(self):
        for index in range(0, len(self.tokens)):
            word = self.tokens[index]
            word_count = self.word_counts[index]
            wordvec = vec(word)
            if wordvec is not None: 
                wordvec = np.insert(wordvec, 0, word_count, axis = 0)
                self.all_vectors = np.insert(
                        self.all_vectors, 
                        self.all_vectors.shape[0], 
                        wordvec,
                        axis = 0
                        )
        return

    def get_weighted_average_vector(self):
        total_words = np.sum(self.all_vectors, axis = 0)[0]
        totals_vector = np.zeros(300)
        for i in range(0, self.all_vectors.shape[0]):
            word_count = self.all_vectors[i][0]
            totals_vector = totals_vector + word_count * self.all_vectors[i][1:301]
        output = totals_vector / total_words
        self.weighted_avg_vector = output
        return