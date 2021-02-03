# -*- coding: utf-8 -*-
import Biterm


class Doc():
    ws = []  
    def __init__(self,s):
        self.ws = [] 

        self.read_doc(s)

    def read_doc(self,s):
        for w in s.split(' '):
            if w != '\n':
                self.ws.append(int(w))
            

    def size(self):
        return len(self.ws)

    def get_w(self,i):
        assert(i<len(self.ws))
        return self.ws[i]


    def gen_biterms(self,bs,docN,win=15):#抽取biterm docN 求θm
            if(len(self.ws)<2):
                return 0 
            if(self.ws.count(self.ws[0]) == len(self.ws) ):
                return 0
            for i in range(len(self.ws)-1):
                for j in range(i+1,min(i+win,len(self.ws))):
                    bs.append(Biterm.Biterm(self.ws[i],self.ws[j],docN))#这里没有判断ws[i]和ws[j]是否相等，所以会出现相同的词组成一个biterm的情况 docN  求θm
            return 1 


if __name__ == "__main__":
    s = '2 3 4 6 1 5'
    d = Doc(s)
    bs = []
    d.gen_biterms(bs)
    for biterm in bs:
        print('wi : ' + str(biterm.get_wi()) + ' wj : ' + str(biterm.get_wj()))