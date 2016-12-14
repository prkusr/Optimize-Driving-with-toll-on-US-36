# encoding: utf8
import codecs
import datetime
import json as j
from collections import defaultdict
import urllib2

FROM_LOC = "fromLocationNameTxt"
TO_LOC = "toLocationNameTxt"
commuteIdMap = dict()

def getCommuteRouteInformation():
    jsonText = ' '.join([line.strip() for line in codecs.open('commuteRoutesJSON.json', 'r', encoding='utf-8')])
    return j.loads(jsonText)


def filterContent(jsonString):
    filteredInfoList = []
    # contentNeededTags = [FROM_LOC,'id',TO_LOC,'viaTxt']
    notNeededTags = ["fromCommuteLocationId","fromMMFlt","orderNum","toCommuteLocationId","toMMFlt"]
    for cRoute in jsonString['CommuteRoute']:
        tempDict = dict(cRoute)
        for c in notNeededTags:
            del tempDict[c]
        filteredInfoList.append(tempDict)

    return filteredInfoList


def getFromToPossibleDestinations(filteredInfo):
    possibleDestinations = defaultdict(list)
    for info in filteredInfo:
        possibleDestinations[info[FROM_LOC]].append(info[TO_LOC])
    return possibleDestinations

def generateCommuteIdHash(filteredInfo):
    tempDict = dict()
    toViaMap = defaultdict(list)
    for info in filteredInfo:
        tempDict[info[FROM_LOC] + "___" + info[TO_LOC] + "___" + info['viaTxt']] = info['id']
        toViaMap[info[FROM_LOC] + "___" + info[TO_LOC]].append(info['viaTxt'])
    return tempDict,toViaMap

def convertToMins(secs):
    secs = int(secs)
    if secs < 0:
        return -1

    s = str(datetime.timedelta(seconds=secs)).split(':')
    calcMin = int(s[1])
    calcMin += 60 * int(s[0])

    if int(s[2]) > 30:
        calcMin += 1

    return calcMin

def getRealTimeData(id):
    urlToHit = 'http://www.cotrip.org/highways/getCommuteRouteInfo.do?commuteRouteId=' + id
    response = urllib2.urlopen(urlToHit).read()
    return j.loads(response)


def getConstraints(information):
    infoList = []
    for l in information['speedRoutes']['CommuteRouteSpeeds']:
        infoList.append(l['Route']['Route'][0])

    constraints = [];
    for info in infoList:
        timeTaken = convertToMins(info['TravelTimeInSeconds'])
        normalTime = int(info['ExpectedTravelTime'][u'Minutes'])
        
        #constraints[info[u'Description']] = [normalTime, timeTaken - normalTime];
        constraints.append((info[u'Description'], normalTime, timeTaken - normalTime))

    return constraints

def scrapData():
    jsonString = getCommuteRouteInformation()
    filteredContent = filterContent(jsonString)
    commuteIdMap,destViaMap = generateCommuteIdHash(filteredContent)
    fromToDest = getFromToPossibleDestinations(filteredContent)
    
    i = 1
    selectionDict = dict()
    for key in fromToDest.keys():
        selectionDict[i] = key
        print str(i) + " : " + key
        i += 1
    
    fromIndex = int(raw_input("Select the starting point :  "))
    src = selectionDict[fromIndex]
    
    i = 1
    selectionDict = dict()
    removeDuplicates =dict()
    
    for dest in fromToDest[src]:
        removeDuplicates[dest] = removeDuplicates.get(dest,0) + 1
    uniqueDest = removeDuplicates.keys()
    
    for i in range(len(uniqueDest)):
        print str(i + 1) + " : " + uniqueDest[i]
    
    index = int(raw_input("Select the destination :  "))
    destination = uniqueDest[index - 1]
    
    via = ''
    if removeDuplicates.get(destination,0) > 1:
        for i in range(0,len(destViaMap[src + '___' + destination])):
            print str(i + 1) + " : " + destViaMap[src + '___' +destination][i]
        index = int(raw_input("Select via :  "))
        via = destViaMap[src + '___' +destination][index - 1]
    else :
        via = destViaMap[src + '___' +destination][0]
    
    # print commuteIdMap[src+'___'+destination+'___'+via]
    information = getRealTimeData(commuteIdMap[src+'___'+destination+'___'+via])
    lpInformation = getConstraints(information)

    #print lpInformation
    return lpInformation
    
#main();