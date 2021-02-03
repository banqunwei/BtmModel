# -*- coding: utf-8 -*-
import time
import re
import sys
import indexDocs
import topicDisplay
import evaluation
import Model
import os

def usage() :

    print("Training Usage: \
    btm est <K> <W> <alpha> <beta> <n_iter> <save_step> <docs_pt> <model_dir>\n\
    \tK  int, number of topics, like 20\n \
    \tW  int, size of vocabulary\n \
    \talpha   double, Parametric Dirichlet prior of P(z), like 1.0\n \
    \tbeta    double, Pymmetric Dirichlet prior of P(w|z), like 0.01\n \
    \tn_iter  int, number of iterations of Gibbs sampling\n \
    \tsave_step   int, steps to save the results\n \
    \tdocs_pt     string, path of training docs\n \
    \tmodel_dir   string, output directory")


def BTM(argvs):
    if(len(argvs)<4):
        usage()
    else:
        if (argvs[0] == "est"):
            K = argvs[1]
            W = argvs[2]
            alpha = argvs[3]
            beta = argvs[4]
            n_iter = argvs[5]
            save_step = argvs[6]
            docs_pt = argvs[7]#id语料库文件名
            dir = argvs[8]
            print("Run BTM: K="+str(K)+", W="+str(W)+", alpha="+str(alpha)+", beta="+str(beta)+", n_iter="+str(n_iter)+", save_step="+str(save_step))
            # 开始时间
            clock_start = time.clock()
            # 主题学习
            thismodel = Model.Model(K, W, alpha, beta, n_iter, save_step)
            thismodel.run(docs_pt,dir)
            # 结束时间
            clock_end = time.clock()
            print("procedure time : "+str(clock_end-clock_start))
        else:
            usage()


if __name__ ==  "__main__":
    K=5
    mode = "est"
    W = None #词典中词汇的个数 词典大小
    alpha = 50/K
    beta = 0.01
    n_iter = 1000 #迭代次数
    save_step = 100 #保存步长
    dir = "../output/"
    input_dir = "../sample-data/"
    model_dir = dir + "model/"
    voca_pt = dir + 'k' +str(K)+ ".voca.txt"  #词汇集合，每行为wordID word 即词典
    dwid_pt = dir + 'k' +str(K)+ "doc_wids.txt"  #文档词汇号集合，每行为wordID wordID...
    doc_pt = input_dir + "fake=0.txt" #文档词汇集合，每行为word word...

    print("=============== Index Docs =============")
    W = indexDocs.run_indexDocs(['indexDocs',doc_pt,dwid_pt,voca_pt]) # W=词典中词汇的个数 词典大小
    print("W : "+str(W))

    argvs = []
    argvs.append(mode)
    argvs.append(K)
    argvs.append(W)
    argvs.append(alpha)
    argvs.append(beta)
    argvs.append(n_iter)
    argvs.append(save_step)
    argvs.append(dwid_pt)
    argvs.append(model_dir)

    print("=============== Topic Learning =============")
    BTM(argvs)

    print("=============== Topic Display =============")
    topicDisplay.run_topicDicplay(['topicDisplay',model_dir, K, voca_pt])
    
    print("=============== Topic Evaluation =============")
    input_filepath = '../output/model/k'+str(K)+'.matrix_zw'
    input_matrix =evaluation.read_matrix_zw(input_filepath)
    evaluation.simlarity(input_matrix,K)
    
    
    