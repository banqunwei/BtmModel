# -*- coding: utf-8 -*-
import math
class Perplexity:
     
    def read_pz(self,pzfile):
     return [float(p) for p in open(pzfile).readline().split()]
 
    def read_pzw(self, pzwfile):
      delta = []
      for l in open(pzwfile):
          vs = [float(v) for v in l.split()]
          delta.append(vs)
          
      return delta
    
  
    def compute_perplexity(self,pzfile,pzwfile,bs):
        pz = self.read_pz(pzfile)
        pzw = self.read_pzw(pzwfile)
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
     
