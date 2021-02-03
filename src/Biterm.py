# -*- coding: utf-8 -*-
class Biterm():
    wi = 0
    wj = 0
    z = 0
    docN=0 #求θm

    def __init__(self,w1=None,w2=None,docNm=None,s=None): # docN 求θm
#        if w1 != None and w2 != None: #这里没有判断ws[i]和ws[j]是否相等  会造成一个biterm中两个词有可能相同。
        if w1 != None and w2 != None and w1 != w2: #增加不相等过滤
            self.wi = min(w1,w2)
            self.wj = max(w1,w2)
            self.docN=docNm # docN 求θm
        elif w1 == None and w2 == None and s != None:
            w = s.split(' ')
            self.wi = w[0]
            self.wj = w[1]
            self.z = w[2]
            if w[3] != None: # docN 求θm
                self.docN=w[3] # docN 求θm

    def get_wi(self):
        return self.wi

    def get_wj(self):
        return self.wj
    
    def get_docN(self):   # docN 求θm
        return self.docN   # docN 求θm

    def get_z(self):
        return self.z

    def set_z(self,k):
        self.z = k

    def reset_z(self):
        self.z = -1

    def str(self):
        _str = ""
        _str += str(self.docN)+"-"+str(self.wi) + '\t' + str(self.wj) + '\t\t' + str(self.z) # docN 求θm
        return _str