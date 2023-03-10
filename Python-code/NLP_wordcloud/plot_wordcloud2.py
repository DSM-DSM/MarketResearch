# -*- coding: utf-8 -*-            
# @Time : 2023/1/1 19:30
# @Author : JinYueYu
# Description : 
# Copyright JinYueYu.All Right Reserved.
import jieba
import pandas as pd
import codecs
from wordcloud import WordCloud
import PIL
import numpy as np
import matplotlib.pyplot as plt

# 载入文本
df = pd.read_excel('../data/深夜食堂/NLP处理后.xlsx')
data = df[df['if_positive'] == 1]

# 载入停用词表
stopwords = [line.strip() for line in
             codecs.open('../../data/cn_stopwords.txt', 'r', encoding='utf-8').readlines()]

# 保存全局分词，用于词频统计
segments = []

for index, row in data.iterrows():
    content = row['short']
    words = jieba.lcut(content, cut_all=False)

    for word in words:
        # 停用词判断，非停用词才记录
        if word not in stopwords:
            segments.append({'word': word, 'count': 1})

# 将结果数组转为dataframe
seg_df = pd.DataFrame(segments)

# 词频统计
word_df = seg_df.groupby('word')['count'].sum()
word_df = word_df.drop([' '])

result = word_df.sort_values(ascending=False)

# 导出频率前300的关键词
result[:300].to_excel('../data/深夜食堂/word_frequency.xlsx', encoding='utf-8')

# 制作词云图
image_background = PIL.Image.open('../../pic/背景/background8.jpg')

MASK = np.array(image_background)
wc = WordCloud(font_path='msyh.ttc', colormap='PuOr', mode='RGBA', scale=2,
               background_color='white', relative_scaling=0.5, height=600, width=800, margin=1,
               max_words=200, min_font_size=20, max_font_size=400, font_step=2, mask=MASK).fit_words(result[0:300])
plt.imshow(wc)
plt.show()
wc.to_file('../pic/原图/蛋糕1/wordcloud15.png')
