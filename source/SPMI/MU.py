import os
import numpy as np
import pandas as pd
import argparse
import math

def WriteFile(lstMI, outputPath):
    wfile = open(outputPath, 'a')
    for row in lstMI:
        for column in row[:-1]:
            wfile.writelines(str(column) + ',')
        wfile.writelines(str(row[-1]) +'\n')
    wfile.close()

def ComputeLamda(x,y):
    x_domain = np.unique(x)
    y_domain = np.unique(y)

    minX = 0
    for k in range(len(x_domain)):
        sx = x[x == x_domain[k]]
        px = len(sx) / len(x)
        if px > 0:
            if px > minX:
                minX = px
    lambda1 = minX

    py_list = {}
    for k in range(len(y_domain)):
        sy = y[y == y_domain[k]]
        py = len(sy) / len(y)
        py_list[y_domain[k]] = py

    return lambda1, py_list

class MU:
    def ComputeMu(pathFileCSV_MI, pathToWrite, minSea, minDen, n):
        mi_df = pd.read_csv(pathFileCSV_MI)
        columns_name = mi_df.columns
        result_final = []
        for att1 in columns_name:
            column1 = mi_df[att1].to_numpy()
            for att2 in columns_name:
                column2 = mi_df[att2].to_numpy()
                lambda1, lambda3Dic = ComputeLamda(column1, column2)
                if lambda1 == 1:
                    lambda1=0.5
                try:
                    muMin = 100

                    for i in lambda3Dic:
                        lambda3 = lambda3Dic[i]
                        v = (minSea * minDen) / (lambda3 * n)

                        if v <= 1 / math.e:
                            mu = 1 - lambda3 / (math.e * np.log(2) * np.log2(1/lambda1))
                        else:
                            mu = 1 - v * lambda3 * np.log2(v) / (np.log(2) * np.log2(lambda1))

                        if mu < muMin:
                            muMin = mu
                except OverflowError:
                    print('OverflowError')

                if muMin >= 1:
                    muMin = 0.99
                stratt = att1 +'-' + att2
                lst = [stratt, muMin]
                result_final.append(lst)

        pathEachSeaDen = pathToWrite  + '_minSea' + str(minSea) + '_minDen' + str(minDen)
        basedir_detail = os.path.dirname(pathEachSeaDen)
        if basedir_detail:
            if not os.path.exists(basedir_detail):
                os.makedirs(basedir_detail)
        if os.path.exists(pathEachSeaDen):
            os.remove(pathEachSeaDen)
        WriteFile(result_final, pathEachSeaDen)

parser = argparse.ArgumentParser(description="MU")
parser.add_argument('-i', '--input', help='input', required=True)
parser.add_argument('-o', '--output', help='output', required=True)
parser.add_argument('-s', '--minSea', help='seasonal occurence', required=True)
parser.add_argument('-d', '--minDen', help='density', required=True)
parser.add_argument('-n', '--DSEQ', help='DSEQ size', required=True)
args = vars(parser.parse_args())
pathInput = args['input']
pathOutput = args['output']
minSea = int(args['minSea'])
minDen = int(args['minDen'])
n = int(args['DSEQ'])
MU.ComputeMu(pathInput, pathOutput, minSea, minDen, n)