# -*- coding: utf-8 -*-
import math
class Theta_m2():
    
 M = 0 
 biterm_docs=[]
 
 def __init__(self,docN):
     self.M = docN  # 文档数目 
     self.biterm_docs=[]
     for i in range(self.M):
         biterm_doc=[]
         self.biterm_docs.append(biterm_doc)
 
 def dividBiterm_docs(self, bs):
     for biterm in bs:
         m=biterm.get_docN()
         self.biterm_docs[m].append(biterm)
         
 def compute_pzm(self, m, pz, pzw):
    biterm_doc = self.biterm_docs[m]
    Bm_N=len(biterm_doc) 
    p_zm = []
    for z in range(len(pz)):
        p = 0 # p(z|d)
        for i in range(Bm_N):
            w1 = biterm_doc[i].wi
            w2 = biterm_doc[i].wj
            p_bi=0 
            for k in range(len(pz)):
                p_bi += pz[k] * pzw[k][w1]*pzw[k][w2]
            p +=  ((pz[z] * pzw[z][w1] * pzw[z][w2]) / p_bi)  
        p /=Bm_N   
        p_zm.append(p)
    return p_zm
            
            
        
 def read_pz(self,pzfile):
     return [float(p) for p in open(pzfile).readline().split()]
 
 def read_pzw(self, pzwfile):
      delta = []
      for l in open(pzwfile):
          vs = [float(v) for v in l.split()]
          delta.append(vs)
          
      return delta
  
 def computeAll_pzm(self, bs, pzfile,pzwfile,pzmfile):
     self.dividBiterm_docs(bs)
     pz = self.read_pz(pzfile)
     pzw = self.read_pzw(pzwfile)
     wf = open(pzmfile,'w')
     for m in range(self.M):
         p_zm = self.compute_pzm(m, pz, pzw)
         for k in range(len(pz)):
             wf.write(str(p_zm[k]) + ' ')
         wf.write("\n")
     wf.close()
    
    #计算训练集的困惑度，并返回
     return self.compute_perplexity(pz,pzw,bs)

 # 顺便计算困惑度
 def compute_perplexity(self,pz,pzw,bs):
        K = len(pz)
        p_B = 0
        for bi in bs:
            w1 = bi.get_wi()
            w2 = bi.get_wj()
            p_bi = 0
            for z in range(K):
               p_bi += pz[z] * pzw[z][w1] * pzw[z][w2] 
            
            p_B += math.log(p_bi)
        return math.exp (-p_B / len(bs))
                
                
        
    
        
     
         
        
        