import nltk
import pandas as pd
import string

#nltk.download()

from nltk import word_tokenize
from nltk.corpus import stopwords
stop_words = set(stopwords.words("english"))

filename = "120925072020.csv"
words_file = "glove.840B.300d_words.csv"

df_data = pd.read_csv(filename)[["IsPhishing", "body_text"]]
df_words = pd.read_csv(words_file)
all_words = df_words["Words"].tolist()
manual_removal = ["n", "nn"]

df_processed = pd.DataFrame(columns = ["IsPhishing", "body_readable"])

for index in range(len(df_data)):
    text = df_data.loc[index][1]   
    tokens = word_tokenize(text)
    tokens = [w.lower() for w in tokens]
    table = str.maketrans("", "", string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    words = [word for word in stripped if word.isalpha()]
    words_no_stop = [w for w in words if not w in stop_words]
    words_only_legit = [w for w in words_no_stop if w in all_words]
    words_only_legit = [w for w in words_no_stop if not w in manual_removal]
    separator = " "
    value = separator.join(words_only_legit)
    df_processed.loc[index, "IsPhishing"] = df_data.loc[index, "IsPhishing"]
    df_processed.loc[index, "body_readable"] = value
    
df_processed.to_csv("processed_" + filename, index = False)