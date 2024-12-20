import pandas as pd

def ReadData(path):
    dataframe = pd.read_excel(path)
    print("Read data Success")
    return dataframe