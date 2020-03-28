# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 14:02:21 2018

@author: Thomas Massion
  make_pnts() generates a pnt txt file with the lat and lon for each county'''
"""
import csv

# INPUT: 1) full path to county csv file from the most recent US census 
#        2) string of state of interested in TWO LETTER abbreviation (e.g. 'FL', 'IL', 'TN', etc)
# ** Instructinos if you do not have most recent csv file:
#       1. go to https://www.census.gov/geo/maps-data/data/gazetteer2017.html
#       2. find the "Counties" tab
#       3. click "Download the National Counties Gazetteer File (139KB)"
#       4. import this file as a tab delimited file to Excel
#       5. save this in excel as a CSV file
# OUTPUT: PNT file of lat and lons per county in special format for degrib-ing

def make_pnts(gazpath,state):

    # ****NOTE: this is necessary for degrib-ing only lats and lons of interest
    
    # read geoID lat and lon through the gazetteer file
    with open(gazpath,'r') as f:
        readCSV = csv.reader(f,delimiter=',')
        state = state.upper()
        
        #  and write into correct pnt file format for state of interest
        with open('pnts'+state+'.txt' ,'w') as f2:
            next(readCSV)
            writeCSV = csv.writer(f2, delimiter=',')
            for row in readCSV:
                if row[0] == state:
                    # pnts file must be in format: label,lat,lon
                    # **the "label" doesn't matter but I use the GEO_ID of the county
                    writeCSV.writerow([row[2],float(row[8]),float(row[9])])  
    return

make_pnts('C:/ndfd/2017_Gaz_counties_national.csv','FL')
make_pnts('C:/ndfd/2017_Gaz_counties_national.csv','NC')
