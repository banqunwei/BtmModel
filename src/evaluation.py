import pandas as pd
import numpy as np
import math
import tf_iwf
import tf_idf


def read_matrix_zw(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:

        wordlist = []
        worddict = {}
        topiclist = []
        K = 0
        n = 0
        for line in f.readlines():
            K += 1
            res = line.split('\t')
            word = res[0]
            if word not in wordlist:
                wordlist.append(word)
                worddict[word] = n
                n += 1

        for i in range(0, int(K/10)): 
            topiclist.append(i)
        matrix_zw = pd.DataFrame(data=0.0, index=topiclist, columns=wordlist)

    f.close()

    with open(filepath, 'r', encoding='utf-8') as f:
        n = 0
        topicID = 0
        for line in f.readlines():
            n += 1
            res = line.split('\t')
            word = res[0]
            wordID = worddict[word]
            weight = res[1]
            # print(topicID,'\t',word,'\t',wordID,'\t',weight)
            if topicID < matrix_zw.shape[0] and wordID < matrix_zw.shape[1]:
                matrix_zw.values[topicID][wordID] = weight
            if n == 10:
                topicID += 1
                n = 0

    f.close()

    return matrix_zw


def simlarity(matrix_zw,K):
    k = matrix_zw.shape[0]  # 行数 主题数K
    print('rows:', k)
    n = matrix_zw.shape[1]  # 列数 词汇数N
    print('columns:', n)
    print(matrix_zw)

    wtssList = []
    btssList = []
    A = 0.0
    B = 1.0
    C = 1.0
    w1 = 0.0
    w2 = 0.0
    wtss = 0.0
    btss = 0.0

    # calculate WTSS
    print('==========WTSS result========')
    for j1 in range(0, n):

        for j2 in range(j1 + 1, n):

            #print('w', j1, '&', 'w', j2)

            for i in range(0, k):
                w1 = matrix_zw.values[i][j1]
                w2 = matrix_zw.values[i][j2]
                # print(w1,'\t',w2)
                A += w1 * w2
                B += math.pow(w1, 2)
                C += math.pow(w2, 2)
            wtss = A / (math.sqrt(B) * math.sqrt(C))
            wtssList.append(wtss)
    

    wtssSum = 0.0
    for item in wtssList:
        wtssSum += item
    wtssFinal = wtssSum/len(wtssList)    


    # calculate BTSS
    print('==========BTSS result========')
    for i1 in range(0, k):
        for i2 in range(i1 + 1, k):
            #print('w', i1, '&', 'w', i2)

            for j in range(0, n):
                w1 = matrix_zw.values[i1][j]
                w2 = matrix_zw.values[i2][j]
                # print(w1,'\t',w2)
                A += w1 * w2
                B += math.pow(w1, 2)
                C += math.pow(w2, 2)
            btss = A / (math.sqrt(B) * math.sqrt(C))
            btssList.append(btss)
    

    btssSum = 0.0
    for item in btssList:
        btssSum += item
    btssFinal = btssSum / len(btssList)    
    
    print('wtssFinal\tbtssFinal')
    print(wtssFinal, btssFinal)
    
    wff = open('../output/model/k'+str(K)+'.finalwtss_btss.txt','w')
    wff.write(str(wtssFinal)+'\t'+ str(btssFinal))
    wff.close()

def write_KS_test(filepath,matrix_zw):

    print('==========Write KS-Test========')

    grouplist = []
    scorelist = []

    K = matrix_zw.shape[0]
    N = matrix_zw.shape[1]

    for i in range(0,K):
        row = matrix_zw.ix[i]
        for j in range(0,N):
            grouplist.append(i)
            scorelist.append(row[j])

    print(grouplist)
    print(len(grouplist))
    print(scorelist)
    print(len(scorelist))

    with open(filepath,'w',encoding='utf-8') as f:

        for i in range(0,len(grouplist)):
            f.write( str(grouplist[i])+'\t'+str(scorelist[i])+'\n' )

    f.close()

