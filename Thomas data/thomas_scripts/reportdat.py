# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 13:31:13 2018

@author: Thomas Massion


'''extracts maximum gust data across at a variety of locations throughout hurricane IRMA
from the official NHC report on the Hurricane. For each latitude and longitude scraped 
the code finds the county for data point and writes the gust, county and lat and lon to a .csv '''

INPUTS: pdf file of the official Hurricane IRMA report

OUTPUTS:
    a csv file containing:
        1) longitude and latitude of each data coordinate
        2) the corresponding county to each coordinate
        3) the max gust recorded at that location throughout the hurricane
"""

import PyPDF2
import csv
import re
import requests


def coord_check(check):
    '''checks if check is a coordinate; returns signed coordinate values if so'''
    if len(check) >= len('(28.54N 81.33W)'):
            check = check.replace(' ','')           
            if (check[6] == 'N' or check[6] == 'S') and \
                (check[12] == 'E' or check[12] == 'W') and (check[13] == ')'):
                # extracting lat and lon from format
                lat = float(check[1:6])
                lon = float(check[7:12])
                if check[6] == 'S':
                    lat = lat*(-1)
                if check[12] == 'W':
                    lon = lon*(-1)
                    return (lat,lon)
        
            else:
                return False
    else:
        return False
    

def find_parens(s):
    '''function that finds all sets of matching paretheses in a string'''
    left_parens  = [i for i,j in enumerate(s) if j == "("]
    right_parens = [i for i,j in enumerate(s) if j == ")"]
        
    if len(left_parens) == len(right_parens):
        pairs = zip(left_parens,right_parens)
       # print('page break: equal')
    elif len(left_parens) > len(right_parens):
        pairs = zip(left_parens[:len(right_parens)], right_parens)
        print('caution: left bigger')
    elif len(left_parens) < len(right_parens):
        pairs = zip(left_parens,right_parens[:len(left_parens)])
        print('caution: right bigger') 
    return list(pairs)


def get_gust(dataline):
    '''extracts gust from a data line, finds county for data point and writes to csv '''
    # must remove parantheses in between sustained wind and gust
    datindxs = find_parens(dataline)
    if len(datindxs) > 0:
        # **removes a space after parentheses as well
        dataline = dataline[:datindxs[0][0]] + dataline[datindxs[0][1]+2:] 
      
        dataline = '--' + dataline + '--'
        print(dataline)
        
        # split apart the nonspace strings from the spaces
        datsplit = re.split("(\s+)",dataline) 
        datacount = 0
        #print(datsplit)
        
        for string in datsplit:
            if string.isspace() == True and len(string) > 2:
                # use length to find out whether gust is present
                datacount += len(string) - 2
                
            # if the string is not empty or a data delimiter
            elif not not string and string != ' ' and string != '  ':  
                # add one to the counter counting up to the gust data
                datacount += 1
                if datacount == 6: # gust is the 5th data entry, now we go to capture the gust
                    gust = float(string)
                    
                    # find the county from API for the lat and lon
                    target_url = 'https://geo.fcc.gov/api/census/area?lat='+str(coord[0])+'&lon='+str(coord[1])+'&format=json'  
                    webtxt = requests.get(target_url).text
                    countyindx = webtxt.find('"county_name":"')
                    countyindx += len('"county_name":"')
                    countyindx2 = webtxt.find('"',countyindx+1)
                    countyname = webtxt[countyindx:countyindx2]
                    if not countyname[0].isalpha():
                        countyname = ''
                    # write the data to csv
                    write.writerow([coord[0],coord[1],countyname,gust])
                    
                    print(gust)
                    print('\n')
                    
        return



# creating a pdf file object
pdfFileObj = open('AL112017_Irma.pdf','rb')

# format notes: 
# - there are two spaces between each data entry
# - a missing entry is represented by a single space
                        
# creating a pdf reader object
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

# printing number of pages in pdf file
#print(pdfReader.numPages)
outlines = pdfReader.getOutlines()
page = pdfReader.getPageLayout()
nump = pdfReader.numPages
xmpdat = pdfReader.getXmpMetadata()

locations = []
txt = ''
counter = 0
last = 0

with open('IrmaExtracted.csv','w',newline='') as f:
    write = csv.writer(f)
    write.writerow(['Latitude','Longitude','County','Gust (kt)'])
    
    # inside for loop: essentially uses the coordinates' format as a delimiter for each line
    for i in range(32,66): # (33,67)
#        if i == 36:
#            break
          
        pageObj = pdfReader.getPage(i)
        page = pageObj.extractText()
        print('\npage break -----------------------\n')
        numpars = len(re.findall('\(',page[265:]))
        page =  page.replace('\n',' ')
        page = page[265:]
        
        # this accounts for a typo on page 36 of the pdf
        # on the second to last coordinate 
        if i == 35:
            page = page[:1154] + "(" + page[1154:]
       
        indxs = find_parens(page)

        # loop through each pair of parentheses and use coord_check
        for j, pair in enumerate(indxs):
#            if j == len(indxs)-1:
#                break  
            forcheck = page[pair[0]:(pair[1]+1)]
            print(pair)
            print(forcheck)
            print(j)
            coord = coord_check(forcheck)
            # print out the full line until next coordinate
            jj = j 
                            # added caveat for if the last line does not have any more parentheses after coordinate
            if coord != False and jj != len(indxs)-1: # in this case coord would have returned a coordinate
                forcheck2 = page[indxs[jj+1][0]:(indxs[jj+1][1]+1)]
                coord2 = coord_check(forcheck2)
                
                while coord2 == False and jj < len(indxs)-1:
                    forcheck2 = page[indxs[jj+1][0]:(indxs[jj+1][1]+1)]
                    coord2 = coord_check(forcheck2)
                    jj += 1

                if coord2 != False:
                    Dataline = page[indxs[j][1]+1:indxs[jj][0]]
                    get_gust(Dataline)

                else:
                    # for the last line of the page
                    Dataline = page[indxs[jj-1][1]+1:len(page)-1]
                    get_gust(Dataline) 
            
        

