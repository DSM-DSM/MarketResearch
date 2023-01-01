# -*- coding: utf-8 -*-            
# @Time : 2023/1/1 15:07
# @Author : JinYueYu
# Description : 
# Copyright JinYueYu.All Right Reserved.
import jieba
import pandas as pd
import numpy as np
import wordcloud
import collections
from wordcloud import WordCloud
from PIL import Image  #
import matplotlib.pyplot as plt

df = pd.read_excel('../data/NLP处理后.xlsx')
df_positive = df[df['if_positive'] == 1]
seg_list = jieba.cut(str(df_positive['short']), cut_all=False)

with open('../data/cn_stopwords.txt', encoding='utf-8') as f:
    con = f.readlines()
    stop_words = set()
    for i in con:
        i = i.replace("\n", "")  # 去掉读取每一行数据的\n
        stop_words.add(i)
result_list = []
for word in seg_list:
    # 设置停用词并去除单个词
    if word not in stop_words and len(word) > 1:
        result_list.append(word)
print(result_list)

# 筛选后统计
word_counts = collections.Counter(result_list)
# 获取前100最高频的词
word_counts_top100 = word_counts.most_common(200)
print(word_counts_top100)

# 绘制词云
my_cloud = WordCloud(
    background_color='white',  # 设置背景颜色  默认是black
    width=900, height=600,
    max_words=100,  # 词云显示的最大词语数量
    font_path='simhei.ttf',  # 设置字体  显示中文
    max_font_size=99,  # 设置字体最大值
    min_font_size=16,  # 设置子图最小值
    random_state=50  # 设置随机生成状态，即多少种配色方案
).generate_from_frequencies(word_counts)

# 显示生成的词云图片
plt.imshow(my_cloud, interpolation='bilinear')
# 显示设置词云图中无坐标轴
plt.axis('off')
plt.show()
