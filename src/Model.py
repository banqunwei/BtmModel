# -*- coding: utf-8 -*-

import numpy as np
import sampler
import pvec
import doc
import Theta_m2
import perplexity



class Model():
    W = 0   # vocabulary size
    K = 0   # number of topics
    n_iter = 0  # maximum number of iteration of Gibbs Sampling
    save_step = 0
    alpha = 0   # hyperparameters of p(z)
    beta = 0    # hyperparameters of p(w|z)

    bs = []    # 存放biterm的集合
    nb_z = pvec.Pvec()   # n(b|z), size K*1  统计在biterm语料库中，每个主题k拥有的biterm数目
    nwz = np.zeros((1, 1))  # n(w,z), size K*W统计在biterm语料库中，字典中每个单词在每个主题k下出现的次数
#    numpy.zeros((2,3)) #创建一维长度为2，二维长度为3的二维元素都是0的数组
    pw_b = pvec.Pvec()   # the background word distribution #统计在（抽取biterm前）原始语
#    料库中，词典中每个词出现的比例  同上上理
    nb_mz = np.zeros((1, 1))  # docN 傅为求θm size M*K统计在每个文档中的biterms在各个主题编号k下的计数
    docN = 0  # 傅为求θm

    def __init__(self, K, W, a, b, n_iter, save_step, has_b=False):
        i=1
        self.bs.clear()
        self.nb_z.clear()
        self.pw_b.clear()
        self.nwz = np.zeros((1, 1))
        self.nb_mz = np.zeros((1, 1))

        self.K = K
        self.W = W
        self.alpha = a
        self.beta = b
        self.n_iter = n_iter
        self.save_step = save_step
        self.has_background = has_b
        self.pw_b.resize(W)  
        self.nwz.resize((K, W))  
        self.nb_z.resize(K)  
        print(self.pw_b.p)
        print(self.nb_z.p)
        print(pvec.Pvec.p)
        print("哈哈哈哈或或或或或或或或或或或或或或哈哈哈哈哈或")
        self.perplexties = [] 

    def run(self, doc_pt, res_dir):

        self.load_docs(doc_pt)  
        self.model_init() 
        print("Begin iteration")  
        out_dir = res_dir + "k" + str(self.K) + "."
        for i in range(1, self.n_iter+1):
            print("\riter "+str(i)+"/"+str(self.n_iter))

            for b in range(len(self.bs)):
                self.update_biterm(self.bs[b]) 

            if i % self.save_step == 0:
                self.save_res(out_dir+str(i))  

        self.save_res(out_dir+"final") 
        print("困惑度列表：") 
        print(self.perplexties)
        print()
        wff = open(out_dir+"plex",'w')
        for plex in self.perplexties:
            wff.write(str(plex)+" ")
        wff.close()
        
        

    def model_init(self):
        for biterm in self.bs:
            k = sampler.uni_sample(self.K)  # 随机为每个biterm生成一个主题编号k
            self.assign_biterm_topic(biterm, k)  # 将该主题编号k指派给该biterm，该biterm的词wi，wj，
#            并计算各个统计量：self.nb_z[k] += 1  self.nwz[k][w1] += 1   self.nwz[k][w2] += 1

    def load_docs(self,docs_pt):

        print("load docs: " + docs_pt)
        rf = open(docs_pt)
        if not rf:
            print("file not found: " + docs_pt)

        for line in rf.readlines():
            d = doc.Doc(line)
            biterms = []
            flag = d.gen_biterms(biterms, self.docN)  #抽取biterms # docN 傅为求θm
            if flag == 1: 
                self.docN+=1 
            for i in range(d.size()):
                w = d.get_w(i)
                self.pw_b[w] += 1 
            for b in biterms:
                self.bs.append(b)

        self.nb_mz.resize((self.docN,self.K)) #傅为求θm
        self.pw_b.normalize()#将计数转换为比例

    def update_biterm(self,bi):#核心算法
        self.reset_biterm_topic(bi)#首先，消除该biterm旧的主题编号在各种统计量的影响，同时将其主题编号置于-1

        # comput p(z|b)
        pz = pvec.Pvec()
        self.comput_pz_b(bi,pz)#其次，用pz向量临时存放该biterm bi用于采样的条件概率分布.此概率分布并没有被归一化

        # sample topic for biterm b
        k = sampler.mul_sample(pz.to_vector())#再次，根据计算出的未归一化的条件概率分布进行主题编号采样
        self.assign_biterm_topic(bi,k)#最后，将采样得到的主题编号k赋给该biterm bi，并更新各个统计量

    def reset_biterm_topic(self,bi):
        k = bi.get_z()
        w1 = bi.get_wi()
        w2 = bi.get_wj()

        self.nb_z[k] -= 1
        self.nwz[k][w1] -= 1
        self.nwz[k][w2] -= 1
        assert(self.nb_z[k] > -10e-7 and self.nwz[k][w1] > -10e-7 and self.nwz[k][w2] > -10e-7)
        bi.reset_z() 

    def assign_biterm_topic(self,bi,k):#指定主题编号，并更新统计量
        bi.set_z(k)
        w1 = bi.get_wi()
        w2 = bi.get_wj()
    
        self.nb_z[k] += 1
        
        self.nwz[k][w1] += 1
        self.nwz[k][w2] += 1

    def comput_pz_b(self,bi,pz):#核心的核心，采样公式计算
        pz.resize(self.K)
        w1 = bi.get_wi()
        w2 = bi.get_wj()

        for k in range(self.K):#条件概率分布

            if (self.has_background and k == 0) :
                pw1k = self.pw_b[w1]
                pw2k = self.pw_b[w2]
            else:
                pw1k = (self.nwz[k][w1] + self.beta) / (2 * self.nb_z[k] + self.W * self.beta)
                pw2k = (self.nwz[k][w2] + self.beta) / (2 * self.nb_z[k] + 1 + self.W * self.beta)

#            pk = (self.nb_z[k] + self.alpha) / (len(self.bs) + self.K * self.alpha)
            pk = (self.nb_z[k] + self.alpha) / (len(self.bs) + self.K * self.alpha-1)
            pz[k] = pk * pw1k * pw2k

    def save_res(self,res_dir):
        pt = res_dir + "pz"
        print("\nwrite p(z): "+pt)
        self.save_pz(pt)

        pt2 = res_dir + "pw_z"
        print("write p(w|z): "+pt2)
        self.save_pw_z(pt2)

        pt3=res_dir + "pz_m2"  
        print("write p(z|m)2傅:"+pt3) 
        self.save_pz_m2(pt,pt2,pt3)  
        
    def save_pz(self,pt):
        pz = pvec.Pvec(pvec_v=self.nb_z)
        pz.normalize(self.alpha)
        pz.write(pt)

    def save_pw_z(self,pt):
        pw_z = np.ones((self.K,self.W))#numpy.ones用来构造全一矩阵
        wf = open(pt,'w')
        for k in range(self.K):
            for w in range(self.W):
                pw_z[k][w] = (self.nwz[k][w] + self.beta) / (self.nb_z[k] * 2 + self.W * self.beta)
                wf.write(str(pw_z[k][w]) + ' ')
            wf.write("\n")

        
    def save_pz_m2(self,pt,pt2,pt3):
        theta_m2=Theta_m2.Theta_m2(self.docN) 
        perplexty=theta_m2.computeAll_pzm(self.bs, pt, pt2, pt3) 
        self.perplexties.append(perplexty)
        
    def save_perplexty(self,pzfile,pzwfile):
       self.perplexties.append( perplexity.Perplexity().compute_perplexity(pzfile,pzwfile, self.bs))