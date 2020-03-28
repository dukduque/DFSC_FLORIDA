# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 09:52:42 2018

@author: Thomas Massion

get_trackdata() creates dictionaries for the realized track data and forecasted track
for any Hurricane using NHC/NOAA Hurricane Advisory Archives

"""


from datetime import timedelta
import datetime
import re
import pickle
from time import strptime
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request

# the following two function are used for text extraction from the NOAA advisory html webpages
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)

# INPUT: storm year and the storm number for that year
#  **storm number can be found from the NHC archives for that year**
# OUTPUT: Extracts the track data and forecasted track data for each NOAA and NHC advisory
def get_trackdata(year,storm_num):
    
    # using this boolean to pass through each advisory
    adv_exists = True

    # initiating dictionaries
    track = dict()
    forecast = dict()

    # zero pad the storm number string for url
    storm_num_str = str(storm_num).zfill(2)
    # intitialize the advisory counter
    adv = 1 
    
    # loop through each advisory while there still is one
    while adv_exists == True:
        
        adv_str = str(adv).zfill(3)
        
        # url format: https://www.nhc.noaa.gov/archive/2018/al06/al062018.fstadv.048.shtml?
        # here the storm number is 6 for Hurricane Florence
        target_url='https://www.nhc.noaa.gov/archive/'+str(year)+'/al'+  \
                storm_num_str+'/al'+storm_num_str+str(year)+'.fstadv.'+adv_str+'.shtml?'  
        
        # using the url format we keep trying to pull advisories until there are none
        try:
            html = urllib.request.urlopen(target_url).read()
        except:
            adv_exists = False
            print('most recent advisory is number:')
            last_adv = adv-1
            print(last_adv)
            break
            
        html = urllib.request.urlopen(target_url).read()
        #print(text_from_html(html))
        webtxt = text_from_html(html)
        
        # get the latitude and longitude of the actual track
        ind_actual = webtxt.find('CENTER WAS LOCATED NEAR ')
        ind_actual += len('CENTER WAS LOCATED NEAR ')
        
        # get the time for the actual track recorded time
        ind_time = webtxt.find('NATIONAL HURRICANE CENTER')
        ind_time += len('NATIONAL HURRICANE CENTER') + 25 # skip to the date and time
        time = int(webtxt[ind_time:ind_time+2])
        
        month = webtxt[ind_time+13:ind_time+16]
        month = strptime(month,'%b').tm_mon
        
        day = int(webtxt[ind_time+17:ind_time+19])
       
        timestamp = datetime.datetime(year,month,day,time)
        # account for 3 hours earlier of advisory for track data (stands for all advisories)
        timestamp -= timedelta(hours=3)
        
        # obtain the lat and lon coordinates for the realized hurricane track
        lat_actual = float(webtxt[ind_actual:ind_actual+4])
        if webtxt[ind_actual+4] == 'S':
            lat_actual = lat_actual*(-1)
        lon_actual = float(webtxt[ind_actual+7:ind_actual+11])
        if webtxt[ind_actual+11] == 'W':
            lon_actual = lon_actual*(-1)
        
        # get the max sustained winds find anywhere within the hurricane
        ind_mw_actual = webtxt.find('MAX SUSTAINED WINDS ')
        ind_mw_actual += len('MAX SUSTAINED WINDS ')
        mw_actual = webtxt[ind_mw_actual:ind_mw_actual+3]
        
        # save the actual track in its place in the dictionary
        track[timestamp] = (float(lat_actual),float(lon_actual),float(mw_actual))
        
        # now extract forecast data
        inds = [m.start() for m in re.finditer('FORECAST VALID',webtxt)]
        inds = [x+len('FORECAST VALID') for x in inds]
        # skip 9 characters to get to lat and lon coordinates
        forecast_timestamp = timestamp + timedelta(hours=12)
        tempdict = dict() # temporary dictionary to make a dictionary of dictionaries
        
        # obtain the first three
        for j in range(0,3):
            lat = float(webtxt[inds[j]+10:inds[j]+14])
            if webtxt[inds[j]+14] == 'S':
                lat = lat*(-1)
            lon = float(webtxt[inds[j]+17:inds[j]+21])
            if webtxt[inds[j]+21] == 'W':
                    lon = lon*(-1)
             
            # forecasted (fc) max winds
            ind_mw_fc = webtxt.find('MAX WIND ',inds[j])
            ind_mw_fc += len('MAX WIND ')
            mw_forecasted = webtxt[ind_mw_fc:ind_mw_fc+3]
            
            ## specified diameters based on forecast time
            if j == 0:
                diameter = 26
            if j == 1:
                diameter = 43
            if j == 2:
                diameter = 56
            
            tempdict[forecast_timestamp] = (lat,lon,diameter,float(mw_forecasted))
            forecast_timestamp += timedelta(hours=12)
            #format=> forecast[timestamp][forecast_timestamp] = (lat,lon)
            
            forecast[timestamp] = tempdict    
            timestamp += timedelta(hours=6)
            
        adv += 1
        #urllib.request.urlclose(target_url)
    
    # dictionary format: track{timestamp: (lat,lon,max_sustained_wind)} 
    with open('track'+str(year)+storm_num_str+'.p','wb') as fp:
        pickle.dump(track, fp, protocol=pickle.HIGHEST_PROTOCOL)
    # dictionary format: forecast{valid_timestamp: forecasted_timestamp: (lat,lon,valid_diameter,max_fc_wind)} 
    with open('forecast'+str(year)+storm_num_str+'.p','wb') as fp2:
        pickle.dump(forecast, fp2, protocol=pickle.HIGHEST_PROTOCOL)
        
    return

# TEST CASES

# Hurricane Florence #6 in 2018 
get_trackdata(2018,6)
# Hurricane Irma  storm #11 in 2017
get_trackdata(2017,11)

    