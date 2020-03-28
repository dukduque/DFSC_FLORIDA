# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 16:22:58 2018

@author: Thomas Massion

depsurge() takes the degribbed outputs for the PSURGE 2.0 data and puts them into
a list of lists format
"""



import pickle


# INPUT: 1) PTSfilepath = Full path for the "floridaPTS.txt" file (example: "C:/ndfd/floridaPTS.txt"):
#                         the PTS's file is a list of coordinates that are used to degrib
#        2) DIRfilepath = Full directory path for the all txt output files (example: "C:/ndfd/degrib/data/fltdat/out/"): ')
#        3) storm name (with a capital first letter such as Irma, Florence, etc)
#        4) surgelvls - a tuple [as in (1,20) ] that indicates the desired range
#                       of surge level data desired (surge abv 2ft,3ft,4ft .. 20ft)
#        5) probability type- either cumulative or incremental storm surge probability
    
# OUTPUT: a list of lists for all the psurge data for each lat and lon from the pntFile over all available advisories
def depsurge(PTSfilepath,DIRfilepath,storm_name,surgelvls,prob_type):
    
    # load advisory time dictionary 
    with open('advisory_times'+storm_name+'.p', 'rb') as op:
        adv_times = pickle.load(op)
    # use length/ points from southeast points into 
   
    psurge = []
    lat = []
    lon = []
    with open(PTSfilepath,'r',newline='\n') as f2: # in format: #label,lat,lon\n
        pnts = [line.split(',') for line in f2]
        n = len(pnts)
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
    
        psurge.append(lat)
        psurge.append(lon)
        
        for adv,value in adv_times.items():
            # if this adivsories data is available we will extract the PSURGE Data
            if value[1] == True:
                sdate = value[0].strftime("%Y%m%d%H")
                # must loop through each surge height as well
                for i in range(surgelvls[0],surgelvls[1]+1): # the official: range(1,21): from prob surge above 1 feet to above 20
                    fname = DIRfilepath + sdate+'_'+storm_name+'_Adv'+str(adv)+'_gt'+str(i)+prob_type+'_agl.grb.txt'
                    with open(fname,'r') as f:
                        for i, line in enumerate(f):
                            # since psurge samples every six hours and has forecasts every six hours
                            # we can simply take the first line from the degribbed output file
                            if i == 1:
                                psurge.append(line.split(', '))
                                break
                # increment the time by six hours
    
    # here we save the list of lists in a pickle file
    with open('de_psurge.p', 'wb') as fp:
          pickle.dump(psurge, fp, protocol=pickle.HIGHEST_PROTOCOL)
          
    return psurge

psurgeout = depsurge('C:/python/pntsFL.txt','C:/python/psurge_files/grbout/','Irma',(1,10),'cum')




## use length/ points from southeast points into 
#    counter = 0 
#    psurge = []
#    lat = []
#    lon = []
#    with open(PTSfilepath,'r',newline='\n') as f2: # in format: #label,lat,lon\n
#        pnts = [line.split(',') for line in f2]
#        n = len(pnts)
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
#        psurge.append(lat)
#        psurge.append(lon)
#        
#        # establish the starting time
#        dt = datetime.datetime(2017,9,7,12) # starting date
#        
#        # loop through each advisory file in the DIRfilepath directory
#        # which corresponds to a specific "datetime" - these psurge files are both 
#        # downloaded and degribbed using psurgesh.sh


#        for z in range(34,52): # the official: range(34,52): # advisories available from psurge (adv 34 to adv 51)
#            sdate = dt.strftime("%Y%m%d%H")
#            # must loop through each surge height as well
#            for j in range(1,21): # the official: range(1,21): from prob surge above 1 feet to above 20
#                fname = DIRfilepath + sdate + '_Irma_Adv' + str(z) + '_gt' + str(j) + '_cum_agl.txt' 
#                with open(fname,'r') as f:
#                    for i, line in enumerate(f):
#                        # since psurge samples every six hours and has forecasts every six hours
#                        # we can simply take the first line from the degribbed output file
#                        if i == 1:
#                            psurge.append(line.split(', '))
#                            break
#            # increment the time by six hours
#            dt = dt + timedelta(hours=6)


#    
#    # here we save the list of lists in a pickle file
#    with open('de_wndspd.p', 'wb') as fp:
#          pickle.dump(psurge, fp, protocol=pickle.HIGHEST_PROTOCOL)
