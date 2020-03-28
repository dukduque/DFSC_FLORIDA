#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 23:54:44 2019

@author: haoxiangyang
"""

import pickle
import sys
from os import path
import csv
import datetime

sys.path.append(path.abspath('/Users/haoxiangyang/Desktop/Git/daniel_Diesel'))  # home
sys.path.append(path.abspath('/home/haoxiang/daniel_Diesel'))  # Crunch

# load the alternative comparison
outDict = {}
outDict["surgeD"] = []
outDict["nomD"] = []
outDict["totalD"] = []
dataAlt = pickle.load(open("/Users/haoxiangyang/Desktop/Git/daniel_Diesel/output/Test_FR50_H96_F72_R24_N24_REAL.p","rb"))
surgeT = 0
nomT = 0
Tlen = 456
for i in range(Tlen):
    surgeT += dataAlt[1][0][i]
    nomT += dataAlt[1][1][i]
    outDict["surgeD"].append([dataAlt[4][i],surgeT])
    outDict["nomD"].append([dataAlt[4][i],nomT])
    outDict["totalD"].append([dataAlt[4][i],surgeT + nomT])
for dType in ["GEFS","NDFD","GAVG","REAL"]:
    dataAlt = pickle.load(open("/Users/haoxiangyang/Desktop/Git/daniel_Diesel/output/Test_FR50_H96_F72_R24_N24_{}.p".format(dType),"rb"))
    surgeT = 0
    nomT = 0
    for i in range(Tlen):
        surgeT += dataAlt[0][0][i]
        outDict["surgeD"][i].append(surgeT)
        nomT += dataAlt[0][1][i]
        outDict["nomD"][i].append(nomT)
        outDict["totalD"][i].append(surgeT + nomT)
    print("---------------- {} -------------------".format(dType))
    print(" & ", round(sum(dataAlt[0][0])/1000,1), " & ", round(sum(dataAlt[0][1])/1000,1), " & ", round((sum(dataAlt[0][0]) + sum(dataAlt[0][1]))/1000,1),\
          " & ", round(sum(dataAlt[2][0]),1), " & ", round(sum(dataAlt[2][1]),1), " & ", round(sum(dataAlt[2][1])+sum(dataAlt[2][0]),1))

title = ["Datetime","TotalD","GEFS","NDFD","GAVG","REAL"]
for i in ["surge","nom","total"]:
    printAdd = "/Users/haoxiangyang/Desktop/Git/daniel_Diesel/output/{}24.csv".format(i)
    fo = open(printAdd,'w',newline = '')
    csvWriter = csv.writer(fo,dialect = 'excel')
    csvWriter.writerow(title)
    csvWriter.writerows(outDict["{}D".format(i)])
    fo.close()
    
# print alternative comparion for R = 12, N = 12
outDict = {}
outDict["surgeD"] = []
outDict["nomD"] = []
outDict["totalD"] = []
dataAlt = pickle.load(open("/Users/haoxiangyang/Desktop/Git/daniel_Diesel/output/Test_FR50_H96_F72_R12_N12_REAL.p","rb"))
surgeT = 0
nomT = 0
Tlen = 444
for i in range(Tlen):
    surgeT += dataAlt[1][0][i]
    nomT += dataAlt[1][1][i]
    outDict["surgeD"].append([dataAlt[4][i],surgeT])
    outDict["nomD"].append([dataAlt[4][i],nomT])
    outDict["totalD"].append([dataAlt[4][i],surgeT + nomT])
for dType in ["GEFS","NDFD","GAVG","REAL"]:
    dataAlt = pickle.load(open("/Users/haoxiangyang/Desktop/Git/daniel_Diesel/output/Test_FR50_H96_F72_R12_N12_{}.p".format(dType),"rb"))
    surgeT = 0
    nomT = 0
    for i in range(Tlen):
        surgeT += dataAlt[0][0][i]
        outDict["surgeD"][i].append(surgeT)
        nomT += dataAlt[0][1][i]
        outDict["nomD"][i].append(nomT)
        outDict["totalD"][i].append(surgeT + nomT)
    print("---------------- {} -------------------".format(dType))
    print(" & ", round(sum(dataAlt[0][0])/1000,1), " & ", round(sum(dataAlt[0][1])/1000,1), " & ", round((sum(dataAlt[0][0]) + sum(dataAlt[0][1]))/1000,1),\
          " & ", round(sum(dataAlt[2][0]),1), " & ", round(sum(dataAlt[2][1]),1), " & ", round(sum(dataAlt[2][1])+sum(dataAlt[2][0]),1))

title = ["Datetime","TotalD","GEFS","NDFD","GAVG","REAL"]
for i in ["surge","nom","total"]:
    printAdd = "/Users/haoxiangyang/Desktop/Git/daniel_Diesel/output/{}12.csv".format(i)
    fo = open(printAdd,'w',newline = '')
    csvWriter = csv.writer(fo,dialect = 'excel')
    csvWriter.writerow(title)
    csvWriter.writerows(outDict["{}D".format(i)])
    fo.close()
    
    
print("---------------- Best -------------------")
dataPPI = pickle.load(open("/Users/haoxiangyang/Desktop/Git/daniel_Diesel/output/Test_FR50_H528_F72_R24_N24_REAL.p","rb"))
print(" & ", round(sum(dataPPI[0][0])/1000,1), " & ", round(sum(dataPPI[0][1])/1000,1), " & ", round((sum(dataPPI[0][0]) + sum(dataPPI[0][1]))/1000,1),\
      " & ", round(sum(dataPPI[2][0]),1), " & ", round(sum(dataPPI[2][1]),1), " & ", round(sum(dataPPI[2][1])+sum(dataPPI[2][0]),1))

# load the S comparison
for i in [24,48,72]:
    dataF = pickle.load(open("/Users/haoxiangyang/Desktop/Git/daniel_Diesel/output/Test_FR50_H96_F{}_R24_N24_GEFS.p".format(i),"rb"))
    print("---------------- {} -------------------".format(i))
    print(" & ", round(sum(dataF[0][0])/1000,1), " & ", round(sum(dataF[0][1])/1000,1), " & ", round((sum(dataF[0][0]) + sum(dataF[0][1]))/1000,1),\
      " & ", round(sum(dataF[2][0]),1), " & ", round(sum(dataF[2][1]),1), " & ", round(sum(dataF[2][1])+sum(dataF[2][0]),1))

# load the F comparison
for i in [96,120,144]:
    dataS = pickle.load(open("/Users/haoxiangyang/Desktop/Git/daniel_Diesel/output/Test_FR50_H{}_F{}_R24_N24_GEFS.p".format(i,i-72),"rb"))
    print("---------------- {} -------------------".format(i))
    print(" & ", round(sum(dataS[0][0])/1000,1), " & ", round(sum(dataS[0][1])/1000,1), " & ", round((sum(dataS[0][0]) + sum(dataS[0][1]))/1000,1),\
      " & ", round(sum(dataS[2][0]),1), " & ", round(sum(dataS[2][1]),1), " & ", round(sum(dataS[2][1])+sum(dataS[2][0]),1))

# load the H comparison
for i in [96,72,48]:
    dataH = pickle.load(open("/Users/haoxiangyang/Desktop/Git/daniel_Diesel/output/Test_FR50_H{}_F24_R24_N24_GEFS.p".format(i),"rb"))
    print("---------------- {} -------------------".format(i))
    print(" & ", round(sum(dataH[0][0])/1000,1), " & ", round(sum(dataH[0][1])/1000,1), " & ", round((sum(dataH[0][0]) + sum(dataH[0][1]))/1000,1),\
      " & ", round(sum(dataH[2][0]),1), " & ", round(sum(dataH[2][1]),1), " & ", round(sum(dataH[2][1])+sum(dataH[2][0]),1))

# load the R comparison
for i in [24,12,6]:
    dataR = pickle.load(open("/Users/haoxiangyang/Desktop/Git/daniel_Diesel/output/Test_FR50_H96_F24_R{}_N24_GEFS.p".format(i),"rb"))
    print("---------------- {} -------------------".format(i))
    print(" & ", round(sum(dataR[0][0])/1000,1), " & ", round(sum(dataR[0][1])/1000,1), " & ", round((sum(dataR[0][0]) + sum(dataR[0][1]))/1000,1),\
      " & ", round(sum(dataR[2][0]),1), " & ", round(sum(dataR[2][1]),1), " & ", round(sum(dataR[2][1])+sum(dataR[2][0]),1))

# load the N comparison
for i in [24,12,6]:
    dataN = pickle.load(open("/Users/haoxiangyang/Desktop/Git/daniel_Diesel/output/Test_FR50_H96_F24_R24_N{}_GEFS.p".format(i),"rb"))
    print("---------------- {} -------------------".format(i))
    print(" & ", round(sum(dataN[0][0])/1000,1), " & ", round(sum(dataN[0][1])/1000,1), " & ", round((sum(dataN[0][0]) + sum(dataN[0][1]))/1000,1),\
      " & ", round(sum(dataN[2][0]),1), " & ", round(sum(dataN[2][1]),1), " & ", round(sum(dataN[2][1])+sum(dataN[2][0]),1))

# load the alpha comparison
for i in [100,50,20]:
    dataalpha = pickle.load(open("/Users/haoxiangyang/Desktop/Git/daniel_Diesel/output/Test_FR{}_H96_F24_R24_N24_GEFS.p".format(i),"rb"))
    print("---------------- {} -------------------".format(i))
    print(" & ", round(sum(dataalpha[0][0])/1000,1), " & ", round(sum(dataalpha[0][1])/1000,1), " & ", round((sum(dataalpha[0][0]) + sum(dataalpha[0][1]))/1000,1),\
      " & ", round(sum(dataalpha[2][0]),1), " & ", round(sum(dataalpha[2][1]),1), " & ", round(sum(dataalpha[2][1])+sum(dataalpha[2][0]),1))
