import pandas as pd
import math

file_dir = "D:/Bachelor_Thesis/Labelled_Emails_Features_Only/Word_Vectors/"
filename = "nan_removed"
PART_1_SIZE = 0.8

df = pd.read_csv(file_dir + filename + ".csv")
#df = df.sample(frac=1).reset_index(drop=True)
#df = df.drop(columns = "Unnamed: 0")
row_count = len(df)
split_at = math.floor(row_count * PART_1_SIZE)

part_1 = df[0 : split_at]
part_2 = df[split_at :]

part_1.to_csv(file_dir + "part_1.csv", index = False)
part_2.to_csv(file_dir + "part_2.csv", index = False)