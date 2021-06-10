'''对输入的中文文本进行文本摘要'''
'''使用无监督的抽取式方法'''

import jieba  #引入用户分词的类
from math import sqrt   #求平方根
import numpy as np  #生成矩阵
import networkx as nx   #构建词网
import PySimpleGUI as sg

class Summarizer():
    '''摘要器的类'''
    def __init__(self):
        self.sentences=[]   #存储从文章中读出来的每一句话
        self.cutSentences=[]    #存储分过词后的每句话
        self.stopwords=[]       #存储中文stopWords
        self.summarize=[]       #存储最后生成的摘要
    
        self.MakeStopwords('cn_stopwords.txt')  #制作stopwords
    
    def MakeStopwords(self,stopfile):
        #读入stopwords词典
        with open(stopfile,'r',encoding='utf-8') as datas:
            lines=datas.readlines()
            for line in lines:
                line=line.strip()
                self.stopwords.append(line)
            
    def load_article(self,filename):
        #获取文章并处理
        writeTo=open(filename+'oneline.txt','w',encoding='utf-8')
        with open(filename,'r',encoding='utf-8') as article:
            lines=article.readlines()
            for line in lines:  #把每一个line都写到新的文件里
                line=line.strip()
                writeTo.write(line)
        writeTo.close()
        #对新造出的堆积在一行的文件进行操作
        with open(filename+'oneline.txt','r',encoding='utf-8') as article:
            line=article.readline()    #只有一行
            sentCuts=line.split('。')   #把每句话都隔开
            for sent in sentCuts:
                self.sentences.append(sent)     #把每句话都加到sentences列表中
  
    def sentSeg(self):
        #对sentences列表进行分词
        for sent in self.sentences:
            seg_list=jieba.cut(sent)
            seg_list=list(seg_list) #将jieba生成的Token转换为列表
            #print(seg_list)
            self.cutSentences.append(seg_list)
        self.cutSentences.pop() #把最后的空列表弹出
        #print(self.cutSentences)

    def makeSimilarityMatrix(self):
        #创建并填入相似度矩阵
        self.sentenceSimilarityMatrix=np.zeros((len(self.cutSentences),len(self.cutSentences)))   #创建空矩阵

        for index1 in range(len(self.cutSentences)):
            for index2 in range(len(self.cutSentences)):
                if index1==index2:
                    continue    #如果两句话相同则不进行比较
                self.sentenceSimilarityMatrix[index1][index2]=self.calcCosineSimilarity(self.cutSentences[index1],self.cutSentences[index2])
    def cosine_distance(self,u, v):
        #返回两个向量的cosine相似度
        return 1 - (np.dot(u, v) / (sqrt(np.dot(u, u)) * sqrt(np.dot(v, v))))
    def calcCosineSimilarity(self,sent1,sent2):
        #采用计算Cosine相似度的方法来计算两个句子的相似度
        
        all_words=list(set(sent1+sent2))    #构造两句话中出现的单词的集合
        vector1=[0]*len(all_words)      #构造两个句子的空词向量
        vector2=[0]*len(all_words)

        #计算词向量
        for word in sent1:
            if word in self.stopwords:
                continue
            vector1[all_words.index(word)]+=1   #出现的词使对应位置向量加1
        for word in sent2:
            if word in self.stopwords:
                continue
            vector2[all_words.index(word)]+=1   
        cosineSim=1- self.cosine_distance(vector1,vector2)
        return cosineSim
    
    def MakeSimilarityGraph(self):
        #根据相似矩阵构建词图
        self.sentenceSimilarityGraph=nx.from_numpy_array(self.sentenceSimilarityMatrix) 
    
    def RankWords(self):
        #根据词图产生权重并排名
        wordScores=nx.pagerank(self.sentenceSimilarityGraph)
        self.ranked=sorted(((wordScores[i],s) for i,s in enumerate(self.cutSentences)),reverse=True)   #依据分数进行排序
    
    def MakeSummary(self,sent_amount):
        #生成摘要,sent_amount为指定的摘要句子总数，默认为3句
        for i in range(sent_amount):
            self.summarize.append(self.ranked[i])
        
        #print(self.summarize)
        #对列表形式进行处理
        output=''
        for sent in self.summarize:
            #print(sent)
            for word in sent[1]:
                output+=str(word)
            output+='。'
        print('下面是对输入文章进行的摘要：')
        print(output)

    
    def generate_summary(self,filename,sent_amount=3):
        #将方法整合起来
        self.load_article(filename)
        self.sentSeg()
        self.makeSimilarityMatrix()
        self.MakeSimilarityGraph()
        self.RankWords()
        self.MakeSummary(sent_amount)

if __name__ == "__main__":           
    test=Summarizer()
    test.generate_summary('myreport.txt',4)


