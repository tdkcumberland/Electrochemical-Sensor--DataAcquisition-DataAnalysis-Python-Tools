#AUTOMATIC BATCH PROCESS SCRIPT FOR ACETONE GAS SENSOR RESPONSE 

#This script extracts the sensor response data from the CSV files output by the KeySight DMM BenchVue Software. 
#The script is capable of process all the CSV files in a batch mode within a specified directory.
#NOTE: the user should have administrative level previlige when running this script since there is read and write procedure that may requires such permission
#Python version: 3.6.6rc1
#Dependencies: Scipy stack 

#Created by: Timothy Cumberland
#Email: tdkcumberland@gmail.com
#Last edited: June 22, 2018

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def find_nearest(array, value): #this function seeks and finds a user defined value closest to value within a specified array
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

data_list = [] #initialize an array to hold the results to be later appended to a dataframe
    
directory=("[Path]") #user can specify the directory containing the CSV files
for root,dirs,files in os.walk(directory):
    for file in files:
        newdirectory = os.path.join(directory,file)
        newdata = pd.read_csv(newdirectory, sep =',', header = 5, names = ["SamplerNumber", "Time", "Data", "Empty"], infer_datetime_format=True)
        #--data preprocessing--#
        newdata.Data = newdata.Data*1e6 #convert the current response to from nA to uA

        newdata['Time'] = pd.to_datetime(newdata['Time'])    #format time stamp to total second elapsed
        newdata['Time'] = newdata['Time'] - newdata['Time'][0]
        newdata['Time'] = newdata['Time'].dt.total_seconds()

        #newdata.plot(x="Time",y="Data") #user can use this code segment to graph the resonse curve
        #plt.show()
        
        #--data analysis--#
        peak_value = max(newdata.Data) #find peak value and its index
        peak_index = newdata.index[newdata['Data'] == peak_value].tolist()
        
        tempdata = newdata['Data'][peak_index[0]:-1] # create a temporary data set starting from the peak till end
        
        three_8th_peak = 3/8*peak_value #find 3/4 and 3/8 peak values and their indexes 
        three_4th_peak = 3/4*peak_value
        three_8th_peak = find_nearest(tempdata, three_8th_peak)
        three_4th_peak = find_nearest(tempdata, three_4th_peak)
        
        three_8th_peak_index = tempdata.index[tempdata == three_8th_peak].tolist()
        three_4th_peak_index = tempdata.index[tempdata == three_4th_peak].tolist()

        #calculate the 3/8 and 3/4 area
        three_8th_area = np.trapz(y = np.asarray(newdata['Data'][:three_8th_peak_index[0]]), x = np.asarray(newdata['Time'][:three_8th_peak_index[0]]))
        three_4th_area = np.trapz(y = np.asarray(newdata['Data'][:three_4th_peak_index[0]]), x = np.asarray(newdata['Time'][:three_4th_peak_index[0]]))
        
        #calculate total area
        total_area = three_4th_area + 2*(three_8th_area - three_4th_area)
        #print([three_8th_area, three_4th_area, total_area])
        data_list.append([peak_value,total_area])
        
output_df = pd.DataFrame(data_list, columns = ['Peak (uA)','Area (uA s)' ]) #output the results into a dataframe with properly formatted column headings
output_df.to_csv(directory, sep = '\t') #the output results are exported into a new CSV file within the same directory
