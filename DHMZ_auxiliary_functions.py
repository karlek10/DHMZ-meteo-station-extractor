# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 08:39:44 2020

@author: karlo
"""
import pandas as pd


def df_editor_meteo(filename):
    df = pd.read_table(filename,  encoding='utf-8', header=None, dtype=str, engine='python')
    df = df[0].str.extract('(.{0,7})' * 13)
    df = df.replace("       ","    NaN", regex=True).replace("(\s)\.(\s)", "0.0", regex=True)
    return df

def df_editor_precip(filename):
    df = pd.read_table(filename,  encoding='utf-8', header=None, dtype=str, engine='python')
    df = df.replace("       ","   NaN ", regex=True).replace("(\s)\.(\s)", "0.0", regex=True).replace("Ponis"," NaN ", regex=True).replace("-","NaN", regex=True)
    df = df[0].str.rstrip().str.split(n=13, expand=True)
    return df


def extract_max_temp(station, df): #REQUIRED: station name string, dataframe with data i.e. d_frames['bednja']
    data_type_idxes = df[df[3] == "   MAKS"].index.values #gets all index values when word "MAKSIMALNA" is found
    ser_max_temp = pd.DataFrame()    
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
            ser_max_temp = ser_max_temp.append(ser).T.squeeze().rename("Max temp [°C] - {}".format(station.capitalize()))
            continue
        idx += 47 # "jumps" to next year
    start_year = pd.to_datetime(df[10][data_type_idxes[0]+1]) # finds the starting year
    dates = pd.date_range(start_year, periods=len(ser_max_temp), freq='1D') # creates the date indexes according to start_year and length of dataframe
    ser_max_temp.index = dates   #converts the indexes to dd.mm.yyyy format
    return ser_max_temp #returns the series of data


def extract_min_temp(station, df): #defines the function which extracts min air temp
    data_type_idxes = df[df[3] == "   MINI"].index.values
    ser_min_temp = pd.DataFrame()
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
            ser_min_temp = ser_min_temp.append(ser).T.squeeze().rename("Min temp [°C]- {}".format(station.capitalize())) #converts the series to df, renames the column
            continue
        idx += 47 # "jumps" to next year
    start_year = pd.to_datetime(df[10][data_type_idxes[0]+1])
    dates = pd.date_range(start_year, periods=len(ser_min_temp), freq='1D')
    ser_min_temp.index = dates   
    return ser_min_temp

def extract_wind_speed(station, df): # defines the function which extracts wind speed
    data_type_idxes = df[df[2] == "   SRED"].index.values
    ser_wind_speed = pd.DataFrame()
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
            ser_wind_speed = ser_wind_speed.append(ser).T.squeeze().rename ("Wind speed [m/s]- {}".format(station.capitalize()))
            continue
        idx += 47
    start_year = pd.to_datetime(df[10][data_type_idxes[0]+1])
    dates = pd.date_range(start_year, periods=len(ser_wind_speed), freq='1D')
    ser_wind_speed.index = dates  
    return ser_wind_speed

def extract_rel_hum(station, df): #defines the function which extracts relative humidity as decimal value
    data_type_idxes = df[df[8] == "LAGA"].index.values
    ser_rel_hum = pd.DataFrame()
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
            ser = (df[i][st_idx:end_idx].astype(dtype = float)) / 100
            ser_rel_hum = ser_rel_hum.append(ser).T.squeeze().rename("Relative humidity [-]- {}".format(station.capitalize()))
            continue
        idx += 47
    start_year = pd.to_datetime(df[12][data_type_idxes[0]+1])
    dates = pd.date_range(start_year, periods=len(ser_rel_hum), freq='1D')
    ser_rel_hum.index = dates   
    return ser_rel_hum

def extract_meteo_precip(station, df): #defines the function which extracts daily precipitation
    data_type_idxes = df[df[4] == "NA OBOR"].index.values
    ser_precip = pd.DataFrame()   
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
            ser_precip = ser_precip.append(ser).T.squeeze().rename("Precip [mm]- {}".format(station.capitalize()))
            continue
        idx += 40
    start_year = pd.to_datetime(df[12][data_type_idxes[0]+1][-4:])
    dates = pd.date_range(start_year, periods=len(ser_precip), freq='1D')
    ser_precip.index = dates
    return ser_precip

def extract_precip(station, df): #defines the function which extracts daily precipitation
    data_type_idxes = df[(df[6] == "oborine") | (df[5] == "oborine")].index.values
    ser_precip = pd.DataFrame()
    for idx in data_type_idxes:
        st_idx = idx + 2
        year = [df[10][idx] if df[10][idx] is not None else df[9][idx]][0]
        for i in df.columns[1:]:
            month = df[i-1][st_idx-1]
            if month == "FEB" and float(year) % 4 != 0: #iterates over columns, each month has different number of rows
                end_idx = st_idx + 28
            elif month == "FEB":
                end_idx = st_idx + 29
            elif month == "APR" or month == "JUN" or month == "SEP" or month == "NOV":
                end_idx = st_idx + 30
            else:
                end_idx = st_idx + 31
            ser = df[i][st_idx:end_idx].astype(dtype = float)
            ser_precip = ser_precip.append(ser).T.squeeze().rename("Precip [mm]- {}".format(station.capitalize()))
            continue
        idx += 36
    start_year = [df[10][data_type_idxes[0]] if df[10][data_type_idxes[0]] is not None else df[9][data_type_idxes[0]]][0]
    dates = pd.date_range(start_year, periods=len(ser_precip), freq='1D')
    ser_precip.index = dates
    return ser_precip