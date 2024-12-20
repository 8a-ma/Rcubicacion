from ImportData import ImportData
from ExportData import ExportData
from CleanFolder import CleanFolder
import pandas as pd
import numpy as np
import datetime

from os.path import exists, join
from os import mkdir, environ
import glob

def extractData(ruta):
    all_files = glob.glob(join(ruta, '*.xlsx'))

    array_Dataframes = []

    for file in all_files:
        df = pd.read_excel(file)
        array_Dataframes.append(df)

    df_final = pd.concat(array_Dataframes,axis=0, ignore_index=True)

    print('Extract Success')

    return(df_final)

def cleanData(dataframe):
    dataframe = dataframe.drop(dataframe.columns[0], axis=1)

    dataframe = dataframe[dataframe['Cantidad'].notna()]
    dataframe = dataframe[dataframe['Cantidad'] != 'na']


    dataframe['Datos'] = dataframe['Datos'].replace(0, np.nan)

    print('Clean Success')

    return dataframe

def transformData(dataframe):
    df = dataframe.copy()
    #Se agrupan por valor de la columna Item y se suma
    df_groupby = df.groupby(['Item', 'Dimensión'], as_index=False).sum()

    # #Se obtienen los valores que no se agruparon, en un nuevo data frame
    df_items_by_group = df_groupby.Item.unique()
    df_items = df.Item.unique()
    df_items_unique = df_items[~np.isin(df_items, df_items_by_group)]

    df_unique = dataframe.loc[dataframe['Item'].isin(df_items_unique)]
    
    # #Se juntan ambas tablas
    df_final = pd.concat([df_groupby, df_unique])
    
    # #Detalles finales
    df_final.index = range(0, len(df_final.index))
    df_final.sort_values('Item')

    print('Transform Success')

    return df_final
    
def CreateFile(dataframe, file_name, folder_path):
    dataframe.to_excel(f'{folder_path}' + f'{file_name}')
    print('Create File Success')
 
def Orchestador2(Data):
    
    if not exists("/tmp/Cubicaciones/"):
        mkdir('/tmp/Cubicaciones/')

    if not exists("/tmp/Resumen Cubicaciones/"):
        mkdir("/tmp/Resumen Cubicaciones/")

    Cubicaciones_folder_path = "/tmp/Cubicaciones/"
    Resumen_folder_path = "/tmp/Resumen Cubicaciones/"

    # Id de la carpeta en drive Resumenes Semanal Cubicaciones
    folder_id = environ.get("ID_FOLDER_DRIVE_EXPORT_PROC2")

    mime_type = ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]
 
    [(ImportData(file['file_id'], [file['file_name']][0], Cubicaciones_folder_path)) for file in Data]

    data = extractData(Cubicaciones_folder_path)
    data = cleanData(data)
    data = transformData(data)

    time = datetime.datetime.now()
    week = datetime.date(time.year, time.month, time.day).isocalendar().week
    file_name = [f'Resumen Semana {week} {time.day}-{time.month}-{time.year}.xlsx']

    CreateFile(data,file_name[0], Resumen_folder_path)

    ExportData(folder_id, file_name, mime_type, Resumen_folder_path)

    CleanFolder(Cubicaciones_folder_path)
    CleanFolder(Resumen_folder_path)

    return 'Success\n'
