# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 14:55:53 2019

@author: Hugh
"""

#psuedo code
#
#build dataframe of all O/D combos that do not have a value for travel time
#

# to take a look at the first line of the file
# import pandas as pd
# df = pd.read_csv(quant_file, nrows = 2)


import time
start = time.time()

quant_file = 'Data/quant/dis_bustuberail_london_500.csv'
lines_read = 0
lines_wrote = 0
zeros = 0

f = open(quant_file, "r")
out = open("Data/quant/quant_zeros.csv", "w")

out.write(f.readline())
for line in f:
    data = line.split(",")
    if float(data[3]) != 0:
#        lines_read = lines_read + 1
        zeros = zeros + 1
        continue
    
#    skip lines with same o and d
    if str(data[0]) == str(data[1]):
        lines_read = lines_read +1
        continue
    
    out.write(line)
    lines_wrote = lines_wrote + 1
    lines_read = lines_read + 1
#    print("read: ", lines_read, "wrote: ", lines_wrote)
#    printing is slow, but need to check correctness
    
    
print("runtime in seconds: ", time.time() - start)
    
print("read: ", lines_read, "wrote: ", lines_wrote)
print("zeros: ", zeros)


f.close()
out.close() 


#Results: 

#with self loops

#runtime in seconds:  33.74353218078613
#read:  23377225 wrote:  5825329
#zeros:  17551896

    
# no loops
#runtime in seconds:  35.11475610733032
#read:  5825329 wrote:  5820494
#zeros:  17551896

#build dataframe of LSOA's bordering Origin LSOA 
#
#add travel time for each of those LSOA's to DEstination LSOA
#
#Build Dataframe of lsoa's bording destination LSOA
#
#add travel time from Origin LSOA to destination border LSOA's 
#
#take min walking plus transit travel time and use as overall time in main matrix











#import pandas as pd
#import csv
#import geopandas

#quant = 'Data/dis_bustuberail_london500/dis_bustuberail_london500.csv'
#quant = "C:/Users/Hugh\Documents/UCL_CASA_1819/Dissertation/Analysis/Data/quant/dis_bustuberail_london_500.csv"
#subset = open("Data/)

#f = open(quant, "r")




#data = pd.read_csv(quant, nrows = 1)

#
#with open(quant) as file:
#    reader = csv.reader(file, delimiter = ',')
#    df = pd.DataFrame(list(reader))


# easily hits memory limits trying to load into df. 
    
#    process:
#       read line by line, taking only lines with zeros. 
#       any line with a zero, save to a dataframe
#       



#quant = 'Data/dis_bustuberail_london_500.csv'

#quant_data = pd.read_csv(quant)

#
#with open(quant) as f: 
#    content = f.readlines()