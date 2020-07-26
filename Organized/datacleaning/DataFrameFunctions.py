#Set a value in a DataFrame
def WriteToDataFrame(Input, Df_Row, Df_Column, Df_Name):
	Df_Name.loc[Df_Row, str(Df_Column)] = str(Input)

#Get a value in a DataFrame
def GetFromDataFrame(Df_Row, Df_Column, Df_Name):
	Output = Df_Name.loc[Df_Row, str(Df_Column)]
	return Output

#Cut a DataFrame and return it
def CutDataFrame(DataFrame_Name, Startrow, Endrow):
	Sliced_DataFrame = DataFrame_Name[Startrow: Endrow]
	return Sliced_DataFrame

def GetColumnFromDataFrame(DataFrame, Column):
    df = DataFrame
    Selected_Column = df[[Column]]
    return Selected_Column

#Get number of rows
def Get_DataFrame_RowCount(DataFrame_Name):
	return DataFrame_Name.shape[0]

#Get number of columns
def Get_DataFrame_ColCount(DataFrame_Name):
	return DataFrame_Name.shape[1]
