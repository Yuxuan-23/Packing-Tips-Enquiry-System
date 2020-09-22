# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 23:17:14 2020
根据test表，添加同義詞，生成tips总表，object表,
@author: Wangyx
"""
from langconv import *
from nltk.corpus import wordnet as wn
import pandas as pd		
import numpy as np
import synonyms

def getSynset(word,lang):
    word_synset = set()
    if lang=="en":
        word = word.replace(' ', '_')
        synsets = wn.synsets(word)  # word所在的词集列表
        for synset in synsets:
            words = synset.lemma_names()
            for word in words:
                word = word.replace('_', ' ')
                word_synset.add(word)
    else:
        synsets = wn.synsets(word,lang='qcn')  # word所在的词集列表
        for synset in synsets:
            words = synset.lemma_names('qcn')
            for word in words:
                word_synset.add(word)
                
        word = Converter('zh-hans').convert(word)#轉為簡體
        
        synsets = wn.synsets(word,lang='cmn')  # word所在的词集列表
        for synset in synsets:
            words = synset.lemma_names('cmn')
            for word in words:
                word_qcn=Converter('zh-hant').convert(word)#繁體
                #word_synset.add(word)#簡體
                word_synset.add(word_qcn)
    
    return list(word_synset)



df = pd.read_csv('data of tips.csv',encoding='gb18030')

#创建一个空的Dataframe
result =pd.DataFrame(columns=('cid','name'))
df['times']=0
result['times']=0
for index, row in df.iterrows():
    
    cid = row['cid']
    names=row['names']
    if isinstance(names,str)==True:#该类包含名称
        print(cid)
        if(names.find(',')!=-1):
            s_names=names.split(',')
            lang="en"
        else:
            s_names=names.split('、')
            lang="qcn"
        s_names_n=[]#存放全部单词，用于生成names文本
        for s in s_names:#去除前后空格
            s=s.strip()#s為當前詞
            word_list=getSynset(s, lang)
            s_names_n.append(s)
            s_names_n=list(set(s_names_n+word_list))
                
        #print(s_names_n)
        names_text=""
        if len(s_names_n)!=0:
            names_text=names_text+s_names_n[0]
            result=result.append(pd.DataFrame({'cid':[cid],'name':[s_names_n[0]]}),ignore_index=True)

        if lang=="en":
            for i in range(1,len(s_names_n)):
                names_text=names_text+", "+s_names_n[i]
                result=result.append(pd.DataFrame({'cid':[cid],'name':[s_names_n[i]]}),ignore_index=True)
        else:
            for i in range(1,len(s_names_n)):
                names_text=names_text+"、"+s_names_n[i]
                result=result.append(pd.DataFrame({'cid':[cid],'name':[s_names_n[i]]}),ignore_index=True)
        print(names_text)
        df.loc[index,'names']=names_text

df.to_csv("./table/Tips.csv",index=None)
result.to_csv('./table/Objects.csv',index=None)
    