# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 16:31:32 2018

@author: Thomas Massion

# get_powerdat() continuously scrapes https://poweroutage.us/ every 3 hours
# and organizes the output into a pickle-d dictionary 
"""

#from datetime import timedelta
#import time
#import datetime

import threading
from datetime import datetime

import re
import pickle
from bs4 import BeautifulSoup
import urllib2
import os.path

# INPUT: 1) county keys database for each state you wish to scrape outage data from (collected into countylists below) 
#        2) state name such as 'Georgia','South Carolina','North Carolina'
# OUTPUT: US_power.p -> pickle file containing a dictionary of the outage data just as it is organized online
#                       format: state: county: provider: lastupdated: (cust_tracked,cust_out)

def get_powerdat():
    #helpful source: https://srome.github.io/Parsing-HTML-Tables-in-Python-with-BeautifulSoup-and-pandas/
    
    #run this function continuously every 3 hours 
    samplingfreq = 3600*3
    threading.Timer(samplingfreq, get_powerdat).start()
    
    # only create new dictionary if it is not existent in current directory
    if os.path.isfile("US_power.p"):
        US_states = pickle.load( open( "US_power.p", "rb" ) )
    else:    
        US_states = dict()    
    counter = 0

    # loops through each state to scrape
    for statekey, countyIDdict in stateIds.items():
        # loops through each county
        state = dict()    
        for countykey, countyname in stateIds[statekey].items():
            
            target_url = 'https://poweroutage.us/area/county/' + str(countykey)
            print(target_url)
            soup = BeautifulSoup(urllib2.urlopen(target_url)) # soup = BeautifulSoup(html)
            table = soup.find_all('table')[0] # Grab the first table
            county = dict()
            #the loops below fill the county dictionary
            for j,row in enumerate(table.find_all('tr')):
                #print(row.get_text())
                
                columns = row.find_all('td')
                # print('a row : *******************')
                # skip the row of column entry names
                if j > 0:
                    provider = dict()
                    # extract table row entries
                    provider_name = columns[0].get_text()
                    cust_tracked = float(columns[1].get_text().replace(',',''))
                    cust_out = float(columns[3].get_text().replace(',',''))
                    lastupdated = columns[5].get_text()
                    lastupdated = datetime.strptime(lastupdated, '%m/%d/%Y %I:%M:%S %p %Z')
                    
                    # establish whether the output needs to be created or updated
                    if os.path.isfile("US_power.p"):
                        # account for if the state, county or provider is not already in the dictionary
                        if statenames[counter] not in US_states:
                            US_states[statenames[counter]] = dict()
                            US_states[statenames[counter]][countykey] = dict()
                            US_states[statenames[counter]][countykey][provider_name] = dict()
                            
                        if countykey not in US_states[statenames[counter]]:
                            US_states[statenames[counter]][countykey] = dict()
                            US_states[statenames[counter]][countykey][provider_name] = dict()
                        
                        if provider_name not in US_states[statenames[counter]][countykey]:
                            US_states[statenames[counter]][countykey][provider_name] = dict()
                   
                               
                        # in the case the dictionary a certain provider needs just needs to be updated temporally
                        US_states[statenames[counter]][countykey][provider_name][lastupdated] = (cust_tracked,cust_out)  
                        #print('~updated~')
                        print(US_states[statenames[counter]][countykey][provider_name])
                    else:
                        # create a dictionary for each provider with different updated times
                        provider[lastupdated] = (cust_tracked,cust_out)
                        print(provider)
                        # create a dictionary for   
                        county[provider_name] = provider
                        #print('~archived~')
                        
            # county level
            if not os.path.isfile("US_power.p"):
                state[countykey] = county
                #  print(county)
            print('finished county')
            print('\n')
        # state level 
        if not os.path.isfile("US_power.p"):
            US_states[statenames[counter]] = state 
        print('finished state-----------------------------')
        counter += 1
    
    # save dictionary with format:
    # state: county: provider: lastupdated: (cust_tracked,cust_out)
    pickle.dump(US_states, open( "US_power.p", "wb" ))      
    print('-finished archiving US_power.p-') 
    return

clist_txt = []

# INPUTS GO HERE
georgia_counties = 'https://poweroutage.us/area/getcountyoutageinfo?state=Georgia&key=43294023483446453'
scarolina_counties = 'https://poweroutage.us/area/getcountyoutageinfo?state=South%20Carolina&key=43294023483446453'
ncarolina_counties = 'https://poweroutage.us/area/getcountyoutageinfo?state=North%20Carolina&key=43294023483446453'
virginia_counties = 'https://poweroutage.us/area/getcountyoutageinfo?state=Virginia&key=43294023483446453'
countylists = [georgia_counties, scarolina_counties, ncarolina_counties, virginia_counties]
statenames = ['Georgia','South Carolina','North Carolina','Virginia']

countyIds = dict()
stateIds = dict()
# here we aquire the county ids into a dictionary for scraping in get_powerdat()
for i,cc in enumerate(countylists):
    ctxt = urllib2.urlopen(cc).read()

    id_indxs = [m.start() for m in re.finditer('"CountyId":',ctxt)]
    clist_txt.append(ctxt)
    for ID in id_indxs:
         # to find the county ID number
         aID = ID + len('"CountyId":')
         aID2 = ctxt.find(',',aID+1)
         countyId = ctxt[aID:aID2]
         # to find the county name
         cname_indx = ctxt.find('"CountyName":"',aID2)
         cname_indx += len('"CountyName":"')
         cname_indx2 = ctxt.find('"',cname_indx+1)
         countyName = ctxt[cname_indx:cname_indx2]
         # make dictionary entry
         if countyName.isalpha():
             countyIds[countyId] = countyName

    stateIds[cc] = countyIds
    countyIds = {}

# this will repeat every 3 hours
get_powerdat()