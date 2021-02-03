#coding=utf-8

import sys
import pandas as pd

def read_voca(pt):
    voca = {}
    for l in open(pt,'r',encoding='UTF-8'):
        wid, w = l.strip().split('\t')[:2]
        voca[int(wid)] = w
    return voca

def read_pz(pt):
    return [float(p) for p in open(pt).readline().split()]
    
# voca = {wid:w,...}
def dispTopics(pt, voca, pz,K):
    k = 0
    topics = []
    for l in open(pt):
        vs = [float(v) for v in l.split()]
        wvs = zip(range(len(vs)), vs) 
        wvs = sorted(wvs, key=lambda d:d[1], reverse=True) 
        
        tmps = ''.join(['%s\t%f\n' % (voca[w],v) for w,v in wvs[:10]]) 
        topics.append((pz[k], tmps))
        k += 1

    print('p(z)\t\tTop words')
    for p, s in sorted(topics, reverse=True):
        print('%f\t%s' % (p, s))
    
    with open('../output/model/k='+str(K)+'.txt','w',encoding='utf-8') as f:
        for pz, tmps in sorted(topics, reverse=True):#根据p(topic|biterms语料库)来排序
            f.write(str(pz)+'\n')
            f.write(str(tmps))
            print('%f\n%s' % (pz, tmps))
    f.close()

    lines = []
    for l in open(pt):
        vs = [float(v) for v in l.split()]
        wvs = zip(range(len(vs)), vs)
        wvs = sorted(wvs, key=lambda d: d[1], reverse=True)
        for w, v in wvs[:10]: # 选取前10个词汇表示主题
            line = voca[w]+'\t'+str(v)+'\n'
            lines.append(line)

    with open('../output/model/k'+str(K)+'.matrix_zw','w',encoding='utf-8') as f:
        for line in lines:
            f.write(line)
        f.close()


def run_topicDicplay(argv):

    if len(argv) < 4:
        print('Usage: python %s <model_dir> <K> <voca_pt>' % argv[0])
        print('\tmodel_dir    the output dir of BTM')
        print('\tK    the number of topics')
        print('\tvoca_pt    the vocabulary file')
        exit(1)
        
    model_dir = argv[1]
    K = int(argv[2])
    voca_pt = argv[3]
    voca = read_voca(voca_pt)    
    W = len(voca)
    print('K:%d, n(W):%d' % (K, W))

    pz_pt = model_dir + 'k%d.finalpz' % K 
    pz = read_pz(pz_pt)  #读取p(topic|biterms语料库)
    
    zw_pt = model_dir + 'k%d.finalpw_z' % K 
    dispTopics(zw_pt, voca, pz,K)
    
    
    print("------------------------输出p(z|m)分布2：------------------------")
    pmz_pt2 = model_dir + "k%d.finalpz_m2" % K   
    displayDoc_z(pmz_pt2,K)  


def displayDoc_z(pmz_pt,K):     
    
    theta_ms = []  
    for l in open(pmz_pt): 
        vs = [float(v) for v in l.split()] 
        rvs = zip(range(len(vs)), vs) 
        rvs = sorted(rvs, key=lambda d: d[1], reverse=True) 
        tmps = ''.join(['topic%d--%f\t' % (k+1, v) for k, v in rvs[:min(len(rvs), 10)]]) 
        theta_ms.append(tmps) 
    
    i=1
    for theta_m in theta_ms: 
        # f.write()
        print('第%d篇文档：%s' % (i, theta_m))  
        i+=1
