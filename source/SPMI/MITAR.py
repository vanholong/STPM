from SPMI.MIFTPMining import MIFTPMining
from Model import *
import csv
import ast
import time
import os
import json
import psutil


def GetSatisfiedAttributes(MIpath,MUpath):
    satisfiedAtts = {}
    lstMI = []
    with open(MIpath) as reader:
        for row in reader:
            lstMI.append(row)

    dicMu = {}
    with open(MUpath, "r") as csvseq:
        reader = csv.reader(csvseq, delimiter=',')
        csvseq.seek(0, 0)
        for row in reader:
            dicMu[row[0]] = ast.literal_eval(row[1])
    for anMI in lstMI:
        lstSatisfiedMI_AnAtt = {}
        lstAnMI = ast.literal_eval(anMI)
        for mi_anAttribute in lstAnMI[1:]:
            keystr = lstAnMI[0] + '-' + mi_anAttribute[0]
            muThres = dicMu[keystr]
            if mi_anAttribute[1] >= muThres:
                lstSatisfiedMI_AnAtt[mi_anAttribute[0]] = mi_anAttribute[1]
        if len(lstSatisfiedMI_AnAtt) > 0:
            satisfiedAtts[lstAnMI[0]] = lstSatisfiedMI_AnAtt
    return satisfiedAtts

def MITAR(config):
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
    MIpath = config.MIs
    MUpath = config.MUs
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

    satisfiedAtts = GetSatisfiedAttributes(MIpath,MUpath)
    MIFTP = MIFTPMining(database, satisfiedAtts, maxper, minSR, minPS, epsilon, minOverlap, mindist, maxdist, maxPatternSize)

    MIFTP.Find1Event()
    MIFTP.Find2FrequentPatterns()
    MIFTP.FindKFrequentPatterns()

    if not os.path.exists(resultDir):
        os.makedirs(resultDir)

    if savePatterns:
        for level in MIFTP.Nodes:
            list_json_obj = []
            for id in MIFTP.Nodes[level]:
                node = MIFTP.Nodes[level][id]
                if details:
                    json_object = node.to_dict(MIFTP.EventTable, maxper, minPS,
                                               MIFTP.EventInstanceTable)
                else:
                    json_object = node.to_dict(MIFTP.EventTable, maxper, minPS)
                if json_object:
                    list_json_obj.append(json_object)

            with open(os.path.join(resultDir, '{}.json'.format(level)), 'w') as outfile:
                json.dump(list_json_obj, outfile)
