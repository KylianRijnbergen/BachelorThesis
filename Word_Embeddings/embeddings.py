import numpy as np

#This class creates the word embedding matrix.
class Embeddings():
    def __init__(self, path, vector_dimension):
        self.path = path
        self.vector_dimension = vector_dimension
        
    @staticmethod
    def get_coefs(word, *arr):
        return word, np.asarray(arr, dtype = "float32")

    def get_embedding_index(self):
        embeddings_index = dict(self.get_coefs(*o.split(" ")) for o in open (self.path, errors = "ignore"))
        return embeddings_index

    def create_embedding_matrix(self, tokenizer, max_features):
        
        model_embed = self.get_embedding_index()
        
        embedding_matrix = np.zeros((max_features + 1, self.vector_dimension))
        for word, index in tokenizer.word_index.items():
            if index > max_features:
                break
            else:
                try:
                    embedding_matrix[index] = model_embed[word]
                except: 
                    continue
        return embedding_matrix