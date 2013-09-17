#!/usr/bin/python

import sys
import csv
import datetime
import random

filename = '/usr/local/bin/splunkDemoDB-noh.csv'

#Create start and end dates
endDate = datetime.datetime.now()
delta = datetime.timedelta(weeks=19)
startDate = endDate - delta

def createLog( grade ):
    if grade == 'A':
        rnd1 = random.randint(2, 4)
        mean = 20
        sd = 2
        daysOffset = 2
        minOffset = 59
    elif grade == 'B':
        rnd1 = random.randint(1, 3)
        mean = 18
        sd = 3
        daysOffset = 3
        minOffset = 30
    elif grade == 'C':
        rnd1 = random.randint(1, 2)
        mean = 16
        sd = 4
        daysOffset = 4
        minOffset = 20
    elif grade == 'D':
        rnd1 = random.randint(1, 1)
        mean = 14
        sd = 4
        daysOffset = 4#previous value was 4
        minOffset = 10
    elif grade == 'F':
        rnd1 = random.randint(0, 1)
        mean = 12
        sd = 6
        daysOffset = 2#previous value was 5
        minOffset = 5
    weekStartTmp = startDate + datetime.timedelta(days=daysOffset)#Creates a disposable variable for the start of the week
    weekEnd = weekStartTmp + datetime.timedelta(days=7)#Creates a disposable variable for the end of the week
    while weekStartTmp <= weekEnd:
        strStartDate = datetime.datetime.strftime(weekStartTmp, '%m/%d/%Y')
        rnSessionHour = int(abs(random.normalvariate(mean, sd)))
        if rnSessionHour > 23:#Normals procedurally generated values to always be less than 24 
            while rnSessionHour >= 23:
                rnSessionHour = int(abs(random.normalvariate(mean, sd)))
        rnSessionStart = str(rnSessionHour).zfill(2) + ':' + str(random.randint(0, 59)).zfill(2) + ':' + str(random.randint(0, 59)).zfill(2)
        rnSessionEnd = datetime.datetime.strptime(rnSessionStart, '%H:%M:%S') + datetime.timedelta(minutes=random.randint(1, minOffset))
        rnSessionID = str(random.randint(0, 999999)).zfill(6)
        if rnSessionEnd < datetime.datetime.strptime(rnSessionStart, '%H:%M:%S'):#Normals procedurally generated values to avoid session ends before starts
            while rnSessionEnd < datetime.datetime.strptime(rnSessionStart, '%H:%M:%S'):
                rnSessionEnd = rnSessionEnd - datetime.timedelta(minutes=1)
        sessionLength = rnSessionEnd - datetime.datetime.strptime(rnSessionStart, '%H:%M:%S')
        print '{0} {1} Session={2} start user="{3} {4}" id={5}'.format(strStartDate, rnSessionStart, rnSessionID, dbRecord[0], dbRecord[1], dbRecord[9]) 
        print '{0} {1} Session={2} end user="{3} {4}" id={5} duration={6} seconds'.format(strStartDate, datetime.datetime.strftime(rnSessionEnd, '%H:%M:%S'), rnSessionID, dbRecord[0], dbRecord[1], dbRecord[9], sessionLength.seconds)
        weekStartTmp = weekStartTmp + datetime.timedelta(days=daysOffset)

with open(filename, 'rb') as csvfile:
    dialect = csv.Sniffer().sniff(csvfile.read(1024))#figure out the csv dialect
    csvfile.seek(0)
    dbRecords = csv.reader(csvfile, dialect)#read in the csvfile with the dialect
    while startDate <= endDate:
        csvfile.seek(0)#Must reset the pointer on the original csv file back to the beginning or the inner loop will not execute
        for dbRecord in dbRecords:
            createLog( dbRecord[2] )
        startDate = startDate + datetime.timedelta(days=7)
