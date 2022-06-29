from .FTPMining import FTPMining
from .Model import *
from .Model.ps_growth import PatternFinder
import csv
import time
import os
import json
import psutil
import itertools


def createCandidate(candidate_level, pattern):
    length = len(pattern)
    candidate_level_k = list(itertools.permutations(pattern))
    if length not in candidate_level:
        candidate_level[length] = set(candidate_level_k)
    else:
        candidate_level[length].update(candidate_level_k)
    for level in range(length-1, 2-1, -1):
        for candidate in candidate_level_k:
            if level not in candidate_level:
                candidate_level[level] = {candidate[:level]}
            else:
                candidate_level[level].add(candidate[:level])

def encode_baseline_input_database(arr, sep = '~'):
    counter = {}
    result = []
    for item in arr:
        if item not in counter:
            result.append(item)
            counter[item] = 1
        else:
            counter[item] += 1
            result.append(item + sep + str(counter[item]))
    return result

def decode_baseline_patterns(arr, sep = '~'):
    result = []
    for item in arr:
        result.append(item.split(sep)[0])
    return result

def BaseLine(config):
    datapath = config.Dataset
    sid = set()
    database = []
    with open(datapath, "r") as csvseq:
        reader = csv.reader(csvseq)
        csvseq.seek(0, 0)
        for row in reader:
            database.append(row)
            sid.add(int(row[-1]))


    name = config.Name
    resultDir = config.ResultsDir
    maxPatternSize = config.MaxPatternSize
    savePatterns = config.SavePatterns
    epsilon = config.Epsilon
    minOverlap = config.MinOverlap
    maxper = config.MaxPer
    minSR = config.MinSR 
    minPS = config.MinPS
    details = config.InDetails
    mindist = config.Mindist
    maxdist = config.Maxdist

    tdb = {}

    for idx, row in enumerate(database):
        _, _, id_event, sID = row
        sID = int(sID)
        if sID not in tdb:
            tdb[sID] = [id_event]
        else:
            tdb[sID].append(id_event)

    for id in tdb:
        tdb[id] = encode_baseline_input_database(tdb[id])

    pattern_finder = PatternFinder(tdb, maxper, minPS, minSR, maxPatternSize)
    patterns = pattern_finder.find_recurring_patterns()
    
    candidate_level = {}
    for pattern in patterns:
        pattern = decode_baseline_patterns(pattern)
        if len(pattern) > maxPatternSize and maxPatternSize > 0:
            continue
        createCandidate(candidate_level, pattern)

    for key in candidate_level:
        if key > maxPatternSize:
            continue
        candidate_level[key] = list(candidate_level[key])
    
    FTP = FTPMining(database, maxper, minSR, minPS, epsilon, minOverlap, mindist, maxdist, maxPatternSize)

    FTP.Find1Event()
    for level in candidate_level.keys():
        if level == 1:
            continue
        if level == 2:
            FTP.Find2FrequentPatterns(candidate_level[2])
        else:
            FTP.FindKFrequentPatterns(candidate_level[level])

    if not os.path.exists(resultDir):
        os.makedirs(resultDir)

    if savePatterns:
        for level in FTP.Nodes:
            list_json_obj = []
            for id in FTP.Nodes[level]:
                node = FTP.Nodes[level][id]
                if details:
                    json_object = node.to_dict(FTP.EventTable, maxper, minPS,
                                                FTP.EventInstanceTable)
                else:
                    json_object = node.to_dict(FTP.EventTable, maxper, minPS)
                if json_object:
                    list_json_obj.append(json_object)

            with open(os.path.join(resultDir, '{}.json'.format(level)), 'w') as outfile:
                json.dump(list_json_obj, outfile)