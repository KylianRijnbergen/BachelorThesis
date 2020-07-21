from text_preprocessing import TextToTensor
from pipeline import Pipeline
from sklearn.model_selection import train_test_split 
import pickle

# Importing generic python packages
import pandas as pd

Df_Data = pd.read_excel("Fruits.xlsx")[["text", "target"]]

A = list(Df_Data["text"])
B = list(Df_Data["target"])
X_train, X_test, Y_train, y_test = train_test_split(A, B, test_size = 0.2, random_state = 1)
del A, B
     

print("Do you want to train the network? [True/False]): ")
to_train = input()

if to_train == "True":
    print("Do you want to save the model? [True/False]: ")
    to_save = input()
    filename = ""
    if to_save == "True":
        print("How do you want to save the model? [Filename] ")
        filename = input()  
             
    results = Pipeline(
            X_train=X_train,
            Y_train=Y_train,
            embed_path='C:/Users/Kylian Rijnbergen/Documents/TBK/Year_3/Module 12/glove.840B.300d.txt',
            embed_dim=300,
            X_test=X_test,
            Y_test=y_test,
            epochs=10,
            batch_size=12
            )
    if to_save == "True":
        pickle.dump(results, open(filename, 'wb'))
    
else: 
    print("Do you want to load a network? [True/False] ")
    to_load = input()
    if to_load == "True":
        print("Which model do you want to load? [Filename] ")
        filename = input()
        # load the model from disk
        results = pickle.load(open(filename, 'rb'))



TextToTensor_instance = TextToTensor(
tokenizer=results.tokenizer,
max_len=1
)


is_this_a_fruit = "apple"

is_this_a_fruit_nn = TextToTensor_instance.string_to_tensor(is_this_a_fruit)

p_fruit = results.model.predict(is_this_a_fruit_nn)[0][0]

print(p_fruit)

