# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 15:54:27 2018

@author: Thomas Massion

 get_psurge_grbs() finds all the advsiory data available from PSURGE, then downloads 
 all of the desired PSURGE .grb files for degribbing

"""

from datetime import timedelta
import pickle
import datetime
import requests
import urllib.request
from time import strptime
from bs4 import BeautifulSoup
from bs4.element import Comment

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
    

# INPUT: 1) storm name (with a capital first letter such as Irma, Florence, etc)
#        2) storm number -**storm number can be found from the NHC archives for that year** 
#        3) storm year
#        4) surgelvls - a tuple [as in (1,20) ] that indicates the desired range
#                       of surge level data desired (surge abv 2ft,3ft,4ft .. 20ft)
#        5) probability type- either cumulative or incremental storm surge probability
#        6) file destination for the downloaded grb files
    
# OUTPUT:1) all the .grb files desired downloaded directly from PSURGE 2.0
#           online to the file destination of choice
#        2) pickle file of a dictionary of advisory times available for the PSURGE data
#           in format advisory_times{advisory_number: [timestamp_for_advisory,Boolean_for_if_PSURGE_has_the_data]}

def get_psurge_grbs(storm_name,storm_num,year,surgelvls,prob_type,dest):

    # zero pad the storm number string for url
    # using this boolean to pass through each advisory
    adv_exists = True
    storm_num_str = str(storm_num).zfill(2)
    # intitialize the advisory counter
    adv = 1 
    advisory_times = {}
    surgelvls = list(surgelvls)
    # loop through each advisory to see where the advisories end for this particular storm
  
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
         
        # now find if PSURGE has this advisory data
        sdate = timestamp.strftime("%Y%m%d%H")
        # for now only testing for surge levels of 1
        target_url='https://slosh.nws.noaa.gov/psurge2.0/data/'+sdate+'/data/'+sdate+'_'+ \
        storm_name+'_Adv'+str(adv)+'_gt'+str(1)+'_'+prob_type+'_agl.grb'    
        
        # using the url format we keep trying to pull advisories until there are none
        request = requests.get(target_url)
        
        # now that we know what data from the advisories PSURGE has since we can test the URL with the status code
        # this is necessary because PSURGE does not necessarily have data for each advisory from NHC/NOAA
        if request.status_code == 200:
            advisory_times[adv] = [timestamp,True]
            
            # we can write the names of the PSURGE files for automated downloading
            for i in range(surgelvls[0],surgelvls[1]+1): # accounting for non-inclusivity of Python
            # URL format: https://slosh.nws.noaa.gov/psurge2.0/data/2018091512/data/2018091512_Florence_Adv65_gt3_cum_agl.grb
            # URL format: https://slosh.nws.noaa.gov/psurge2.0/data/2017090712/data/2017090712_Irma_Adv34_gt10_cum_agl.grb
                grb_name = dest+sdate+'_'+storm_name+'_Adv'+str(adv)+'_gt'+str(i)+prob_type+'_agl.grb'
                grb_url = 'https://slosh.nws.noaa.gov/psurge2.0/data/'+sdate+'/data/'+sdate+'_'+ \
                            storm_name+'_Adv'+str(adv)+'_gt'+str(i)+'_'+prob_type+'_agl.grb' 
                urllib.request.urlretrieve(grb_url, grb_name)
                    
        else:
            advisory_times[adv] = [timestamp,False]
        adv+=1
    
    # this dictionary to be used for de_psurge.py
    with open('advisory_times'+storm_name+'.p', 'wb') as fp:
        pickle.dump(advisory_times, fp, protocol=pickle.HIGHEST_PROTOCOL)
          
    return advisory_times

adv_times = get_psurge_grbs('Irma',11,2017,(1,10),'cum','C:/python/psurge_files/')




# old code for only IRMA:
#
#    # we use wget to download from these urls being creatd
#    with open('C:/ndfd/psurgenames/psurgeurls.txt','w') as f: #newline=''
#        # the .dat and .ind files create flat file databases from the degribbed files
#        # -- this is not necessary for the current data extraction method but could 
#        # be more efficient than text files in the future
#        with open(r'C:\ndfd\psurgenames\psurgeinds.txt','w') as f2:
#            with open(r'C:\ndfd\psurgenames\psurgedats.txt','w') as f3:
#                with open(r'C:\ndfd\psurgenames\psurgegrbs.txt','w') as f4:
#                    with open(r'C:\ndfd\psurgenames\psurgetxts.txt','w') as f5:
#                        dt = datetime.datetime(2017,9,7,12) # starting date
#                    # here we loop through each advisory number and psurge height 
#                    # in order to have the correct downloaded-able URls and more for 
#                    # the psurgesh.sh shell script
#                    for i in range(34,52): # the official: range(34,52):
#                        for j in range(1,21): # the official: range(1,21):
#                            sdate = dt.strftime("%Y%m%d%H")
#                            
#                            # https://slosh.nws.noaa.gov/psurge2.0/data/2018091512/data/2018091512_Florence_Adv65_gt3_cum_agl.grb
#                            
#                            # for bash on your computer
#                            f.write('https://slosh.nws.noaa.gov/psurge2.0/data/' + sdate + '/data/' + sdate + '_Irma_Adv' + str(i) + '_gt' + str(j) + '_cum_agl.grb') 
#                            f.write('\n')
#                            f2.write('/c/ndfd/degrib/data/fltdat/'+ sdate + '_Irma_Adv' + str(i) + '_gt' + str(j) + '_cum_agl.ind')
#                            f2.write('\n')
#                            f3.write('/c/ndfd/degrib/data/fltdat/'+ sdate + '_Irma_Adv' + str(i) + '_gt' + str(j) + '_cum_agl.dat')
#                            f3.write('\n')
#                            f4.write('/c/ndfd/degrib/data/grbfiles/'+ sdate + '_Irma_Adv' + str(i) + '_gt' + str(j) + '_cum_agl.grb')
#                            f4.write('\n')
#                            f5.write('/c/ndfd/degrib/data/fltdat/out/'+ sdate + '_Irma_Adv' + str(i) + '_gt' + str(j) + '_cum_agl.txt')
#                            f5.write('\n')
#                            
#                            # for xfce on NOVA
#    #                            f.write('https://slosh.nws.noaa.gov/psurge2.0/data/' + sdate + '/data/' + sdate + '_Irma_Adv' + str(i) + '_gt' + str(j) + '_cum_agl.grb') 
#    #                            f.write('\n')
#    #                            f2.write('/home/tmassion/degrib/data/fltdat/'+ sdate + '_Irma_Adv' + str(i) + '_gt' + str(j) + '_cum_agl.ind')
#    #                            f2.write('\n')
#    #                            f3.write('/home/tmassion/degrib/data/fltdat/'+ sdate + '_Irma_Adv' + str(i) + '_gt' + str(j) + '_cum_agl.dat')
#    #                            f3.write('\n')
#    #                            f4.write('/home/tmassion/grbfiles/'+ sdate + '_Irma_Adv' + str(i) + '_gt' + str(j) + '_cum_agl.grb')
#    #                            f4.write('\n')
#    #                            f5.write('/home/tmassion/degrib/data/fltdat/out/'+ sdate + '_Irma_Adv' + str(i) + '_gt' + str(j) + '_cum_agl.txt')
#    #                            f5.write('\n')
#                    print(sdate)
#                    dt = dt + timedelta(hours=6)
                                