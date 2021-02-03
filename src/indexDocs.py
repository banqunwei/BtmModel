# coding=utf-8
import sys
import pandas as pd

w2id = {}
def indexFile(pt, res_pt):
    print('index file: '+str(pt))
    wf = open(res_pt, 'w',encoding='UTF-8')

    for l in open(pt,'r',encoding='UTF-8'):
        ws = l.strip().split() # 每个文档的词汇列表
        for w in ws: # 给词汇编号
            if w not in w2id:
                w2id[w] = len(w2id)  #w2id是字典
        wids = [w2id[w] for w in ws]  #每个文档的词汇编号列表,wids只是临时存放1个文档中所有单词对应的编号，wid是真正存放字典的地方
            # print(wf,' '.join(map(str, wids)))
        print(' '.join(map(str,wids))) #用空格作为间隔符
        wf.write(' '.join(map(str,wids))) # wf/res_pt/dwid_pt表示由单词的id号表示的整个语料库，一行代表1个文档
        wf.write('\n')
         
    print('write file: '+str(res_pt))
    wf.close 

def write_w2id(res_pt):#字典文件

    print('write:'+str(res_pt))
    with open(res_pt,'w',encoding='UTF-8') as wf:
        for w, wid in sorted(w2id.items(), key=lambda d:d[1]):#lambda表达式是起到一个函数速写的作用。允许在代码内嵌入一个函数的定义。
            wf.write('%d\t%s\n' % (wid, w))
            print('%d\t%s' % (wid, w))

#将语料库中的单词string转为id号，重新生成单词id号表示的语料库；建立词典。
def run_indexDocs(argv):

    if len(argv) < 4:
        print('Usage: python %s <doc_pt> <dwid_pt> <voca_pt>' % argv[0])
        print('\tdoc_pt    input docs to be indexed, each line is a doc with the format "word word ..."')
        print('\tdwid_pt   output docs after indexing, each line is a doc with the format "wordId wordId..."')
        print('\tvoca_pt   output vocabulary file, each line is a word with the format "wordId    word"')
        exit(1)
        
    doc_pt = argv[1]
    dwid_pt = argv[2]
    voca_pt = argv[3]
    indexFile(doc_pt, dwid_pt)
    print('n(w)='+str(len(w2id)))
    write_w2id(voca_pt)
    return len(w2id)