#!/usr/bin/env python
# coding: utf-8

# BTM介绍：https://zhuanlan.zhihu.com/p/111545954 <br>
# https://www.zhihu.com/question/298517764 <br>
# https://blog.csdn.net/windows2/article/details/16812363 <br>
# 代码解析：https://zhuanlan.zhihu.com/p/111722915 <br>
# github xiaohuiyan(提出者) : https://gitcode.net/mirrors/xiaohuiyan/BTM?utm_source=csdn_github_accelerator <br>
# github galesour(代码解析 注释版): https://github.com/galesour/BTM <br>
# github(源代码): https://hub.fastgit.xyz/jasperyang/BTMpy

# LDA计算公式：https://www.cnblogs.com/bydream/p/6844499.html <br>
# 困惑度函数：https://blog.csdn.net/xxidaojia/article/details/102702492 <br>
# https://zhuanlan.zhihu.com/p/114432097


import jieba
import os
import re
import numpy as np
import jieba.posseg as psg
import networkx as nx
import pandas as pd
import math

f = open('data/data.txt', encoding='utf-8')
data = f.readlines()
f.close()


def get_stop_dict(file):
    content = open(file, encoding="utf-8")
    word_list = []
    for c in content:
        c = re.sub('\n|\r', '', c)
        word_list.append(c)
    return word_list


stop_file = "data/cn_stopwords.txt"
stop_words = get_stop_dict(stop_file)

f = open('data/data_cutted.txt', 'w', encoding='utf-8')
for t in data:
    t = re.sub('\n', '', t)
    t_seg = psg.cut(t)
    t_seg_f = []
    # flag_list = ['n','nz','vn','v']
    for word_flag in t_seg:
        if len(word_flag.word) > 1 and word_flag.word not in stop_words:
            t_seg_f.append(word_flag.word)
    if len(t_seg_f) > 0:
        t_seg_f = ' '.join(t_seg_f)
        f.write(t_seg_f + '\n')
f.close()

# 关于弹幕类的，网络用语很多。同义词、停用词、
# 关于采样可能有一些变化

"""
#困惑度函数：https://blog.csdn.net/xxidaojia/article/details/102702492
import math
def perplexity(ldamodel, testset, dictionary, size_dictionary, num_topics):
    print('the info of this ldamodel: \n')
    print('num of topics: %s' % num_topics))
    prep = 0.0
    prob_doc_sum = 0.0
    topic_word_list = [] 
    for topic_id in range(num_topics):
        topic_word = ldamodel.show_topic(topic_id, size_dictionary)
        dic = {}
        for word, probability in topic_word:
            dic[word] = probability
        topic_word_list.append(dic)  
    doc_topics_ist = []  
    for doc in testset:
        doc_topics_ist.append(ldamodel.get_document_topics(doc, minimum_probability=0))
    testset_word_num = 0
    for i in range(len(testset)):
        prob_doc = 0.0  # the probablity of the doc
        doc = testset[i]
        doc_word_num = 0  
        for word_id, num in dict(doc).items():
            prob_word = 0.0  
            doc_word_num += num
            word = dictionary[word_id]
            for topic_id in range(num_topics):
                # cal p(w) : p(w) = sumz(p(z)*p(w|z))
                prob_topic = doc_topics_ist[i][topic_id][1]
                prob_topic_word = topic_word_list[topic_id][word]
                prob_word += prob_topic * prob_topic_word
            prob_doc += math.log(prob_word)  # p(d) = sum(log(p(w)))
        prob_doc_sum += prob_doc
        testset_word_num += doc_word_num
    prep = math.exp(-prob_doc_sum / testset_word_num)  # perplexity = exp(-sum(p(d)/sum(Nd))
    print("模型困惑度的值为 : %s" % prep)
    return prep


"""
