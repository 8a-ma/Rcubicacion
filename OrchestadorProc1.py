from ImportData import ImportData
from ExportData import ExportData
from ReadData import ReadData
from CleanFolder import CleanFolder
from os.path import join, exists
from os import mkdir, environ
import pandas as pd
import numpy as np

def CleanData(dataframe):
    # Se extrae el cliente y la dirección
    customer = dataframe.iat[0,0]
    direction = dataframe.iat[1,0]

    # Se eliminan el cliente y la dirección
    dataframe = dataframe.drop([0,1,2])
    
    #Se renombran las columnas
    dataframe.columns = dataframe.iloc[0]
    dataframe.drop(index=3, inplace=True)
    dataframe.columns.name = None
    dataframe.index = range(0, len(dataframe.index))

    #Se eliminan la ubicación de cada material
    mask = dataframe[['Dimensión', 'Medida', 'Cantidad', 'Datos']].isna().all(axis=1)
    dataframe.drop(index=dataframe[mask].index, inplace=True)

    print("Clean Data Success")
    
    return dict(
        dataframe= dataframe, 
        customer= customer, 
        direction= direction
        )

def StandarData(dataframe):
    #Se copian las columnas necesarias
    df = dataframe[['Item', 'Dimensión', 'Cantidad', 'Datos']].copy()

    #Se agrupan por valor de la columna Item y se suman
    df_by_group = df.groupby(['Item', 'Dimensión'], as_index=False).sum()
    dataframe.loc[dataframe.Datos == 0] = None

    #Se obtienen los valores que no se agruparon, en un nuevo data frame
    df_items_by_group = df_by_group.Item.unique()
    df_items = df.Item.unique()
    df_items_unique = df_items[~np.isin(df_items, df_items_by_group)]

    df_unique = df.loc[df['Item'].isin(df_items_unique)]
    
    #Se juntan ambas tablas
    df_final = pd.concat([df_by_group, df_unique])
    
    #Detalles finales
    df_final.index = range(0, len(df_final.index))
    df_final.sort_values('Item')

    print("Standar Data Success")
    
    return df_final

def CreateFile(dataframe, file_name, folder_path):
    dataframe.to_excel(f'{folder_path}' + f'{file_name}')
    print("Create File Success")

def changename(file_name_array):
    name_array = file_name_array.split('.')
    word_add = "Resumen "
    name_array.insert(1, word_add)
    file_name = ""

    for value in name_array:
        point = "."
        if(value == "xlsx" or value == word_add):
            point = ""
        file_name += value + point

    return file_name

def Orchestador1(data):
    
    #CleanFolder('/tmp/')
    if not exists("/tmp/Cubicaciones/"):
        mkdir('/tmp/Cubicaciones/')

    if not exists("/tmp/Resumen Cubicaciones/"):
        mkdir("/tmp/Resumen Cubicaciones/")

    Cubicaciones_folder_path = "/tmp/Cubicaciones/"
    Resumen_folder_path = "/tmp/Resumen Cubicaciones/"

    # Id de la carpeta de drive Resumen Cubicaciones
    folder_id = environ.get("ID_FOLDER_DRIVE_EXPORT_PROC1")

    mime_type = ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]
    file_id = data['file_id']
    file_name = [data['file_name']]    

    ImportData(file_id, file_name[0], Cubicaciones_folder_path)
    
    data = ReadData(join(Cubicaciones_folder_path, file_name[0]))
    data = CleanData(data)["dataframe"]
    data = StandarData(data)

    # Cambio de nombre
    new_name = [changename(file_name[0])]
    
    CreateFile(data, new_name[0], Resumen_folder_path)

    ExportData(folder_id, new_name, mime_type, Resumen_folder_path)

    CleanFolder('/tmp/Cubicaciones/')
    CleanFolder("/tmp/Resumen Cubicaciones/")

    return 'Success\n'
