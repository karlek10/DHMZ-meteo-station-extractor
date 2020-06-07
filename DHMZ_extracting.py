# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 08:34:28 2020

@author: karlo
"""
import glob
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import DHMZ_auxiliary_functions as dhmz_functions


currentDirectory = os.getcwd()


"""
This is an example for extracting data from METEO stations. 
IMPORTANT - select the DATA folder with the METEO stations data
The METEO and PRECIP stations data differ. 
"""

list_files = os.listdir(currentDirectory + "./meteo_data") #folder where the data is located
os.chdir(currentDirectory + './meteo_data')
d_frames={file: dhmz_functions.df_editor_meteo(file) for file in list_files} #extract the dataframes from the meteo files
max_temps_dict = {station: dhmz_functions.extract_max_temp(station, d_frames[station]) for station in list_files}
humidity_dict = {station: dhmz_functions.extract_rel_hum(station, d_frames[station]) for station in list_files}

os.chdir(currentDirectory)

df_humidity = pd.concat(humidity_dict, axis=1)
humidity_stats = df_humidity.describe()

#ploting the data
sns.set()
df_humidity_monthly = df_humidity.resample('M').mean()
_ = df_humidity_monthly.plot(figsize = (10,5))
_ = plt.xlabel('Date')
_ = plt.ylabel('Rel. Humidity [-]')


"""
#example, string with the station name, dataframe of the station --> HOW TO RUN EXTRACTORS
bednja_min_temp = dhmz.extract_min_temp('bednja', d_frames_meteo['bednja']) 
bednja_max_temp = dhmz.extract_max_temp('bednja', d_frames_meteo['bednja'])
    
bednja_oborine = dhmz.extract_meteo_precip ('bednja', d_frames_meteo['bednja'])

ludbreg_wind = dhmz.extract_wind_speed('ludbreg', d_frames_meteo['ludbreg'])

os.chdir(currentDirectory)

bednja_data = {'max_temp': bednja_max_temp}

df = pd.DataFrame(bednja_data)


"""



"""
This is an example for extracting data from PRECIPITATION stations. 
IMPORTANT - select the DATA folder with the METEO stations data
"""
list_files = os.listdir(currentDirectory + "./precip_data") #folder where the data is located
os.chdir(currentDirectory + './precip_data')
d_frames={file: dhmz_functions.df_editor_precip(file) for file in list_files} #extract the dataframes from the meteo files
precip_dict = {station: dhmz_functions.extract_precip(station, d_frames[station]) for station in list_files}
os.chdir(currentDirectory)
df_precip = pd.concat(precip_dict, axis=1)

df_precip_stats = df_precip.describe()

#ploting the data
sns.set()
df_precip_monthly = df_precip.resample('M').sum() #sum of monthly precipitation
_ = df_precip_monthly.plot(figsize = (10,5))
_ = plt.xlabel('Date')
_ = plt.ylabel('Precipitation [mm]')