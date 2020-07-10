from text_preprocessing import TextToTensor
from pipeline import Pipeline
from sklearn.model_selection import train_test_split 

# Importing generic python packages
import pandas as pd

Df_Data = pd.read_excel("Fruit_Non_Fruit_No_Blackberry.xlsx")[["text", "target"]]

A = list(Df_Data["text"])
B = list(Df_Data["target"])
X_train, X_test, Y_train, y_test = train_test_split(A, B, test_size = 0.2, random_state = 1)
     

               
results = Pipeline(
X_train=X_train,
Y_train=Y_train,
embed_path='C:/Users/Kylian Rijnbergen/Documents/TBK/Year_3/Module 12/glove.6B.300d.txt',
embed_dim=300,
X_test=X_test,
Y_test=y_test,
epochs=6,
batch_size=12
)

TextToTensor_instance = TextToTensor(
tokenizer=results.tokenizer,
max_len=2
)

Labels = results.yhat
Acc = results.acc

is_this_a_fruit = "blackberry"

is_this_a_fruit_nn = TextToTensor_instance.string_to_tensor(is_this_a_fruit)

p_fruit = results.model.predict(is_this_a_fruit_nn)[0][0]

print(p_fruit)

