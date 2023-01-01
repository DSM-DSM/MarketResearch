# -*- coding: utf-8 -*-            
# @Time : 2023/1/1 13:39
# @Author : JinYueYu
# Description : 
# Copyright JinYueYu.All Right Reserved.
import pandas as pd
from snownlp import SnowNLP
import re

df = pd.read_excel('../data/孤独的美食家十季度短评处理后.xlsx')

comments = df['short'].tolist()

# 去除一些无用的字符   只提取出中文出来
content = [' '.join(re.findall('[\u4e00-\u9fa5]+', item, re.S)) for item in comments]
not_pop_list = []
for i in range(len(content)):
    if content[i] != '':
        not_pop_list.append(i)
content_new = []
for i in range(len(content)):
    if i in not_pop_list:
        content_new.append(content[i])

# 对每条评论进行情感打分
scores = [SnowNLP(i).sentiments for i in content_new]
df['sentiment_score'] = 0.5
df.loc[not_pop_list, 'sentiment_score'] = scores

threshold = 0.65
print('在正面情绪概率阈值为%s的条件下，正面情绪出现的频率%s' % (
    threshold, sum(df['sentiment_score'] > threshold) / len(df)))

df['if_positive'] = 0
df.loc[df['sentiment_score'] > threshold, 'if_positive'] = 1
df.to_excel('../data/NLP处理后.xlsx')
