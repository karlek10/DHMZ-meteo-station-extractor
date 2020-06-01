# -*- coding: utf-8 -*-
"""
Created on Thu May 28 13:26:52 2020

@author: karlo
"""

import pandas as pd
import os

def df_editor(filename):
    df = pd.read_table(filename,  encoding='utf-8', header=None, dtype=str, engine='python')
    df = df[0].str.extract('(.{0,7})' * 13)
    df = df.replace("       ","    NaN", regex=True).replace("(\s)\.(\s)", "0.0", regex=True)
    return df


def extract_max_temp(station, df): #REQUIRED: station name string, dataframe with data i.e. d_frames['bednja']
    data_type_idxes = df[df[3] == "   MAKS"].index.values #gets all index values when word "MAKSIMALNA" is found
    df_max_temp = pd.DataFrame()    
    for idx in data_type_idxes: #iterates over indexes
        st_idx = idx + 3
        for i in df.columns[1:]:
            month = df[i][st_idx-1]
            if month == "     II" and float(df[10][st_idx-2]) % 4 != 0: #iterates over columns, each month has different number of rows
                end_idx = st_idx + 28
            elif month == "     II":
                end_idx = st_idx + 29
            elif month == "    IV " or month == "    VI " or month == "    IX " or month == "     XI":
                end_idx = st_idx + 30
            else:
                end_idx = st_idx + 31
            ser = df[i][st_idx:end_idx].astype(dtype = float) #creates a series of floats
            df_max_temp = df_max_temp.append(ser).T.squeeze().rename("Max temp [°C] - {}".format(station.capitalize()))
            continue
        idx += 47 # "jumps" to next year
    start_year = pd.to_datetime(df[10][data_type_idxes[0]+1]) # finds the starting year
    dates = pd.date_range(start_year, periods=len(df_max_temp), freq='1D') # creates the date indexes according to start_year and length of dataframe
    df_max_temp.index = dates.strftime('%d.%m.%Y')   #converts the indexes to dd.mm.yyyy format
    return df_max_temp #returns the dataframe


def extract_min_temp(station, df): #defines the function which extracts min air temp
    data_type_idxes = df[df[3] == "   MINI"].index.values
    df_min_temp = pd.DataFrame()
    for idx in data_type_idxes:
        st_idx = idx + 3
        for i in df.columns[1:]:
            month = df[i][st_idx-1]
            if month == "     II" and float(df[10][st_idx-2]) % 4 != 0: #iterates over columns, each month has different number of rows
                end_idx = st_idx + 28
            elif month == "     II":
                end_idx = st_idx + 29
            elif month == "    IV " or month == "    VI " or month == "    IX " or month == "     XI":
                end_idx = st_idx + 30
            else:
                end_idx = st_idx + 31
            ser = df[i][st_idx:end_idx].astype(dtype = float) #creates a series of floats
            df_min_temp = df_min_temp.append(ser).T.squeeze().rename("Min temp [°C]- {}".format(station.capitalize())) #converts the series to df, renames the column
            continue
        idx += 47 # "jumps" to next year
    start_year = pd.to_datetime(df[10][data_type_idxes[0]+1])
    dates = pd.date_range(start_year, periods=len(df_min_temp), freq='1D')
    df_min_temp.index = dates.strftime('%d.%m.%Y')    
    return df_min_temp

def extract_wind_speed(station, df): # defines the function which extracts wind speed
    data_type_idxes = df[df[2] == "   SRED"].index.values
    df_wind_speed = pd.DataFrame()
    for idx in data_type_idxes:
        st_idx = idx + 3
        for i in df.columns[1:]:
            month = df[i][st_idx-1]
            if month == "     II" and float(df[10][st_idx-2]) % 4 != 0: #iterates over columns, each month has different number of rows
                end_idx = st_idx + 28
            elif month == "     II":
                end_idx = st_idx + 29
            elif month == "    IV " or month == "    VI " or month == "    IX " or month == "     XI":
                end_idx = st_idx + 30
            else:
                end_idx = st_idx + 31
            ser = df[i][st_idx:end_idx].astype(dtype = float) #creates a series of floats
            df_wind_speed = df_wind_speed.append(ser).T.squeeze().rename ("Wind speed [m/s]- {}".format(station.capitalize()))
            continue
        idx += 47
    start_year = pd.to_datetime(df[10][data_type_idxes[0]+1])
    dates = pd.date_range(start_year, periods=len(df_wind_speed), freq='1D')
    df_wind_speed.index = dates.strftime('%d.%m.%Y')   
    return df_wind_speed

def extract_rel_hum(station, df): #defines the function which extracts relative humidity as decimal value
    data_type_idxes = df[df[8] == "LAGA"].index.values
    df_rel_hum = pd.DataFrame()
    for idx in data_type_idxes:
        st_idx = idx + 3
        for i in df.columns[1:]:
            month = df[i][st_idx-1]
            if month == "     II" and float(df[12][st_idx-2]) % 4 != 0: #iterates over columns, each month has different number of rows
                end_idx = st_idx + 28
            elif month == "     II":
                end_idx = st_idx + 29
            elif month == "    IV " or month == "    VI " or month == "    IX " or month == "     XI":
                end_idx = st_idx + 30
            else:
                end_idx = st_idx + 31
            ser = df[i][st_idx:end_idx].astype(dtype = float)
            ser = ser / 100
            df_rel_hum = df_rel_hum.append(ser).T.squeeze().rename("Relative humidity [-]- {}".format(station.capitalize()))
            continue
        idx += 47
    start_year = pd.to_datetime(df[12][data_type_idxes[0]+1])
    dates = pd.date_range(start_year, periods=len(df_rel_hum), freq='1D')
    df_rel_hum.index = dates.strftime('%d.%m.%Y')   
    return df_rel_hum

def extract_precip(station, df): #defines the function which extracts daily precipitation
    data_type_idxes = df[df[4] == "NA OBOR"].index.values
    df_precip = pd.DataFrame()   
    for idx in data_type_idxes:
        st_idx = idx + 3
        year = df[12][idx+1][-4:]
        for i in df.columns[1:]:
            month = df[i][st_idx-1]
            if month == "     II" and float(year) % 4 != 0: #iterates over columns, each month has different number of rows
                end_idx = st_idx + 28
            elif month == "     II":
                end_idx = st_idx + 29
            elif month == "    IV " or month == "    VI " or month == "    IX " or month == "     XI":
                end_idx = st_idx + 30
            else:
                end_idx = st_idx + 31
            ser = df[i][st_idx:end_idx].astype(dtype = float)
            df_precip = df_precip.append(ser).T.squeeze().rename("Precip [mm]- {}".format(station.capitalize()))
            continue
        idx += 40
    start_year = pd.to_datetime(df[12][data_type_idxes[0]+1][-4:])
    dates = pd.date_range(start_year, periods=len(df_precip), freq='1D')
    df_precip.index = dates.strftime('%d.%m.%Y')
    return df_precip



#IMPORTANT - select the DATA folder with the meteo stations data
list_files = os.listdir("./data") #folder where the data is located
os.chdir('./data')
d_frames={file: df_editor(file) for file in list_files} #extract the dataframes from the meteo files






#example, string with the station name, dataframe of the station --> HOW TO RUN EXTRACTORS
bednja_min_temp = extract_min_temp('bednja', d_frames['bednja']) 
bednja_max_temp = extract_max_temp('bednja', d_frames['bednja'])
    
bednja_oborine = extract_precip ('bednja', d_frames['bednja'])

ludbreg_wind = extract_wind_speed('ludbreg', d_frames['ludbreg'])












    


