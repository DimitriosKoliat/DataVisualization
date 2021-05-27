import mysql.connector
import csv
import os
from tkinter import filedialog
import tkinter
import itertools
from pathlib import Path

def getAllCountriesAndYears():
    global years, countries
    years = []
    countries = []
    for path in Path("Scripts/data").iterdir():
        if path.is_file():
            f  = open(path, "r")
            filename = f.name
            if(filename.split('.')[1] == "csv" and filename.split('.')[0] != "final"):
                yearsList = f.readline().split(",")
                years = union(years, yearsList)
                yearsList = []
                for line in f:
                    if(line.split(',')[0] not in countries):
                        countries.append(line.split(',')[0])
    if("country" in years):
        years.remove("country")
    years.sort()
    countries.sort()

def getCountries():
    return countries

def getYears():
    return years

def union(list1, list2):
    for x in list2:
        if(x not in list1 and x.split('\n')[0] not in list1):
            list1.append(x.split('\n')[0])
    return list1



def editData():
    finalList = []
    j = 0
    i = 0
    for c in countries:
        k = 0
        for y in years:
            finalList.append([])
            finalList[i].append(j+1)
            finalList[i].append(k+1)
            i += 1
            k += 1
        j += 1
    for a in range(i):
        for b in range(14):
            finalList[a].append("")
    a = 0
    fl = 2
    for path in Path("Scripts/data").iterdir():
        if path.is_file():
            f  = open(path, "r")
        filename = f.name
        i = 0
        if(filename.split('.')[1] == "csv" and filename.split('.')[0] != "final"):
            country = "a"
            year = ""
            print("Loading csv file ", filename)
            yearsList = f.readline().split(',')
            while(country != ""):
                line = f.readline().split(',')
                l = 1
                country = line[0]
                if(country != ""):
                    while(finalList[i][1] != 1):
                        i += 1
                    countryId = countries.index(country) + 1
                    while(countryId > finalList[i][0]):
                        i += 63
                    y = 1
                    while(y != len(yearsList)):
                        year = yearsList[y].split('\n')[0]
                        yearId = years.index(year) + 1
                        while(yearId > finalList[i][1]):
                            i += 1
                        if(yearId == finalList[i][1] and countryId == finalList[i][0]):
                            finalList[i][fl] = line[l].split('\n')[0]
                            l += 1
                        y += 1
            fl += 1
    return finalList


def createFinalFile():
    fileCsv = open('final.csv', mode='w')
    lista = editData()

    fileWrite = csv.writer(fileCsv, delimiter=',',
                           quotechar='"', quoting=csv.QUOTE_MINIMAL)
    fileWrite.writerow(['Countries_C_ID', 'Years_Y_ID', 'Female_industry_workers_percent_of_female_employment', 'Female_long_term_unemployment_rate_percent',
                        'Female_service_workers_percent_of_female_employment',
                        'Happiness_score', 'Human_development_index', 'Indastry_percent_of_gdb',
                        'Industry_workers_percent_of_employment', 'Long_term_unemployment_rate_percent',
                        'Male_industry_workers_percent_of_male_employment', 'Male_long_term_unemployment',
                        'Male_service_workers_percent_of_male_employment',
                        'Manuf_employ', 'Services_percent_of_gdp', 'Service_workers_percent_of_umployment', 'Measure_ID'])
    id = 1
    for i in lista:
        i.append(id)
        fileWrite.writerow(i)
        id += 1
    print("Final file is ready")

def mainTD():
    getAllCountriesAndYears()
    createFinalFile()
