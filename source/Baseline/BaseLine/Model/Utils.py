from .Relation import *
from datetime import *
import math 

class Utils:
    def check_relation(time_a, time_b, label_a, label_b, epsilon, min_overlap):
        relation = None
        if time_a.start == time_b.start:
            if time_a.end == time_b.end:
                if label_a >= label_b:
                    return relation
        elif time_a.start > time_b.start:
            return relation

        if label_a != label_b:
            if time_a.end - epsilon <= time_b.start:
                relation = Relation.Follows
            elif (time_a.start <= time_b.start) and (time_a.end + epsilon >= time_b.end):
                relation = Relation.Contains
            elif (time_a.start < time_b.start) and (time_a.end - epsilon < time_b.end) and (time_a.end - time_b.start >= min_overlap - epsilon):
                relation = Relation.Overlaps
        else:
            if time_a.end - epsilon <= time_b.start:
                relation = Relation.Follows
        return relation

    def checkDistance(IPI, value,  mindist, maxdist):
        if len(IPI) == 0:
            return True
        distance = value - IPI[-1][1]
        if mindist <= distance <= maxdist:
            return True
        return False

    def calculateSR_ESR(sID_list, maxper, minPS, mindist, maxdist):
        sID_list = sorted(sID_list)
        Esr = 0
        IPI = []
        sID_list.append(-1)
        candidate = None
        candidateESR = None

        for value in sID_list:
            if candidateESR is None:
                candidateESR = [value]
            else:                
                perESR = (value) - (candidateESR[-1])
                if  perESR <= maxper:
                    candidateESR.append(value)
                else:
                    Esr += math.floor(len(candidateESR)/minPS)
                    candidateESR = [value]

            if candidate is None:
                if Utils.checkDistance(IPI, value, mindist, maxdist):
                    candidate = [value]
                continue            

            per = (value) - (candidate[-1])
            if  per <= maxper:
                candidate.append(value)
            else:
                ps = len(candidate)
                if ps >= minPS:
                    IPI.append((candidate[0], candidate[-1]))

                if Utils.checkDistance(IPI, value, mindist, maxdist):
                    candidate = [value]
                else:
                    candidate = None 
        Sr = len(IPI) 
        return Sr, Esr

    def getIPI_PS(sID_list, maxper, minPS): 
        sID_list = sorted(sID_list) 
        result = {}
        sID_list.append(-1)
        candidate = [sID_list[0]] 

        for value in sID_list[1:]:
            per = (value) - (candidate[-1])
            if per <= maxper:
                candidate.append(value)
            else:
                ps = len(candidate)
                if ps >= minPS:
                    result[str((candidate[0], candidate[-1]))] = ps
                candidate = [value]   
        return result

    def checkArgs(epsilon, minoverlap, maxpatternsize):
        if 0 > epsilon:
            raise ValueError("epsilon must be larger or equal 0")
        if 0 >= minoverlap:
            raise ValueError("minoverlap must be larger 0")
        if 2 > maxpatternsize:
            if maxpatternsize != -1:
                raise ValueError("maxpatternsize must be larger or equal 2")

    