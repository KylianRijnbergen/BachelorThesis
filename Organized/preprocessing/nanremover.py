import pandas as pd


is_excel = False
file_dir = "D:/Bachelor_Thesis/GitHub/BachelorThesis/Organized/testfiles/"
filename = "vectorized_mails.csv"
df = pd.DataFrame()
if is_excel:
	df = pd.read_excel(file_dir + filename + ".xlsx")
else:
	df = pd.read_csv(file_dir + filename)

try:    
    df = df.drop(columns = "Unnamed: 0")
    df = df.drop(columns = "ID")
except:
    pass

nan_columns = df.isnull().any(axis=1)

rows_list = []

for i in range(0, len(df)):
    if nan_columns.loc[i]:
        rows_list.append(i)

new_df = df.drop(rows_list)

    
new_df.to_csv(file_dir + "nan_removed.csv", index = False)    