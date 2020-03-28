# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 11:23:52 2018

@author: Thomas Massion

dewndspd() takes the degribbed outputs for the NDFD windspeed data and puts them into
a list of lists format
"""


import os
import pickle

# INPUT: 1) PTSfilepath = Full path for the pntFile need to degrib example: ("C:/ndfd/floridaPTS.txt")
#                         the PTS's file is a list of coordinates 
#        2) DIRfilepath = Full directory path for the all txt output files (example: "C:/ndfd/degrib/data/fltdat/out/"): ')
# OUTPUT: a list of lists for all the NDFD wind speed data for each lat and lon from the pntFile over all available advisories

#PTSfilepath = "C:/ndfd/floridaPTS.txt"
def dewndspd(PTSfilepath,DIRpath):
    
    with open(PTSfilepath,'r',newline='\n') as f2: # in format: #label,lat,lon\n
        pnts = [line.split(',') for line in f2]
        n = len(pnts)
        
        # use length/ points from southeast points into 
        wndspd = []
        lat = []
        lon = []
        
        # making data descriptors, eventually to be appended to the "wndspd" list of lists
        lat.append('element')
        lat.append('unit')
        lat.append('refTime')
        lat.append('validTime')
        lon.append('element')
        lon.append('unit')
        lon.append('refTime')
        lon.append('validTime')
        
        # making the lat and lon the headers of the "columns" they correspond to
        for i in range(n):
            lat.append(float(pnts[i][1]))
            lon.append(float(pnts[i][2]))
         
        wndspd.append(lat)
        wndspd.append(lon)

        # for each file in the directory of degribbed output files 
        # - these specific files were downloaded by hand from ndfd however use the 
        # ndfdsh.sh bash shell script to degrib them all into the chosen directory
        for filename in os.listdir(DIRpath):
    
            with open(DIRpath+filename,'r') as f:
                # these are the list of exception reference times that compensate with their forecast(valid) times
                if filename[-8:-4] == '0047' or filename[-8:-4] == '0447'  or \
                    filename[-8:-4] == '1846' or filename[-8:-4] == '1347' or \
                    filename[-8:-4] == '2247' or filename[-8:-4] == '2246' or \
                    filename[-8:-4] == '0746' or filename[-8:-4] == '1247' or \
                    filename[-8:-4] == '1647' or filename[-8:-4] == '1946':  
                    for i, line in enumerate(f):
                        if  i >= 2 and i <=3: # i == 3: #
                            # here we are appending the line data from the degribbed output to the list of lists
                            wndspd.append(line.split(', ')) 
                            #break 
                else:
                    for i, line in enumerate(f):
                        if  i >= 1 and i <= 2: # i == 2:
                            # here we are appending the line data from the degribbed output to the list of lists
                            wndspd.append(line.split(', '))
                            #break
      
    # here we save the list of lists in a pickle file
    with open('de_wndspd.p', 'wb') as fp:
          pickle.dump(wndspd, fp, protocol=pickle.HIGHEST_PROTOCOL)
    return wndspd
  
wndspdout = dewndspd('C:/python/pntsFL.txt',"C:/ndfd/degrib/data/outWndSpd/")
  







#  with open(PTSfilepath,'r',newline='\n') as f2: # in format: #label,lat,lon\n
#        pnts = [line.split(',') for line in f2]
#        n = len(pnts)
#        
#        # making data descriptors, eventually to be appended to the "wndspd" list of lists
#        lat.append('element')
#        lat.append('unit')
#        lat.append('refTime')
#        lat.append('validTime')
#        lon.append('element')
#        lon.append('unit')
#        lon.append('refTime')
#        lon.append('validTime')
#        
#        # making the lat and lon the headers of the "columns" they correspond to
#        for i in range(n):
#            lat.append(float(pnts[i][1]))
#            lon.append(float(pnts[i][2]))
#         
#        wndspd.append(lat)
#        wndspd.append(lon)
#        
#        #DIRpath = 'C:/ndfd/degrib/data/outWndSpd/'
#    
#        # for each file in the directory of degribbed output files 
#        # - these specific files were downloaded by hand from ndfd however use the 
#        # ndfdsh.sh bash shell script to degrib them all into the chosen directory
#        for filename in os.listdir(DIRpath):
#            print(filename[-8:-4])
#            with open(DIRpath+filename,'r') as f:
#                # these are the list of exception reference times that compensate with their forecast(valid) times
#                if filename[-8:-4] == '0047' or filename[-8:-4] == '0447'  or \
#                    filename[-8:-4] == '1846' or filename[-8:-4] == '1347' or \
#                    filename[-8:-4] == '2247' or filename[-8:-4] == '2246' or \
#                    filename[-8:-4] == '0746' or filename[-8:-4] == '1247' or \
#                    filename[-8:-4] == '1647' or filename[-8:-4] == '1946':  
#                    for i, line in enumerate(f):
#                        if  i >= 2 and i <=3: # i == 3: #
#                            # here we are appending the line data from the degribbed output to the list of lists
#                            wndspd.append(line.split(', ')) 
#                            #break 
#                else:
#                    for i, line in enumerate(f):
#                        if  i >= 1 and i <= 2: # i == 2:
#                            # here we are appending the line data from the degribbed output to the list of lists
#                            wndspd.append(line.split(', '))
#                            #break
#      
#    # here we save the list of lists in a pickle file
#    with open('de_wndspd.p', 'wb') as fp:
#          pickle.dump(wndspd, fp, protocol=pickle.HIGHEST_PROTOCOL)
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
#    # making the lat and lon the headers of the "columns" they correspond to
#    for i in range(n):
#            lat.append(float(pnts[i][1]))
#            lon.append(float(pnts[i][2]))
#       
#    wndspd.append(lat)
#    wndspd.append(lon)
#    
#    DIRpath = 'C:/ndfd/degrib/data/outWndSpd/'
#    
#    for filename in os.listdir(DIRpath):
#        #print(filename[-8:-4])
#        with open(DIRpath+filename,'r') as f:
#            # take the third line (the 7-hour out projection since 447 is for 5 am as opposed to 6am)
#            #if filename[-8:-4] == '0447':  
#            next(f)
#            for j, line in enumerate(f):
#                linesplit = line.split(', ')
#                #linesplit = linesplit[4:]
#               # print(linesplit)
#                if j > 1:
#                   break
#                for mm in range(n) :
#                    temp[(lat[mm],lon[mm])] = float(linesplit[mm + 4])
#                
#         
#                # valid time changes with each line
#                validTime = linesplit[3]
#                # put all the lat lon values into a dictionary
#                temp2[validTime] = temp
#            # break
#            
#            refTime = linesplit[2]
#            wspd[refTime] = temp2
#                        
#                    if i == 2:
#                        wndspd.append(line.split(', '))
#                    if i == 3:
#                        wndspd.append(line.split(', '))
#                        break
            # otherwise take the 6-hours-out forecast this is the 2nd line since the windspeed has forecasts for every three hours        
#            else:
#                for i, line in enumerate(f):
#                    if i == 1:
#                        wndspd.append(line.split(', '))
#                    if i == 2:
#                        wndspd.append(line.split(', '))
#                        break
    # refTime changes with each file

    
            
    # do your stuff

    
    
#    dt = datetime.datetime(2017,9,7,12) # starting date
#    for z in range(34,52): # the official: range(34,52): # advisories available from psurge (adv 34 to adv 51)
#        sdate = dt.strftime("%Y%m%d%H")
#        for j in range(1,21): # the official: range(1,21): from prob surge above 1 feet to above 20'
#            # format:  YCDZ98_KWBN_201709071146
#            fname = "C:/ndfd/degrib/data/outWndSpd/" + sdate + '_Irma_Adv' + str(z) + '_gt' + str(j) + '_cum_agl.txt' 
#            with open(fname,'r') as f:
#                for i, line in enumerate(f):
#                    if i == 1:
#                        psurge.append(line.split(', '))
#                        break
#
#        dt = dt + timedelta(hours=6)
