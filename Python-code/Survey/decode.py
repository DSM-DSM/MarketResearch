# -*- coding: utf-8 -*-            
# @Time : 2023/2/9 23:00
# @Author : JinYueYu
# Description : 
# Copyright JinYueYu.All Right Reserved.
import pandas as pd
import numpy as np


def get_map_dict():
    map = pd.read_excel('../../data/data.xlsx', sheet_name='文本编码对照表')
    r, c = map.shape[0], map.shape[1]
    idx = map[0].isnull()
    idx = idx[idx == False].index.to_list()
    idx.append(r)
    for i in range(30):
        for j in range(r):
            if idx[i] <= map.iloc[j, :].name < idx[i + 1]:
                map.iloc[j, 0] = map.iloc[idx[i], 0]
    groups = map.groupby(0)
    map_dict = dict()
    for key, group in groups:
        single_question = dict()
        single_question['question'] = group.iloc[0, 1]
        single_question['question_type'] = group.iloc[0, 2]
        for i in range(group.shape[0] - 2):
            single_question[group.iloc[i + 2, 1]] = group.iloc[i + 2, 2]
        map_dict[key] = single_question
    return map_dict


def decoding_centroids(question, coder):
    map_dict = get_map_dict()
    coder = coder.astype(int)
    if len(coder) != len(question):
        import warnings
        warnings.warn('输入长度不一致！！')
        return
    else:
        string = str()
        for i in range(len(coder)):
            string += map_dict[question[i]][str(coder[i])] + ','
        string = string.rstrip(',')
        print(string)


def decoding_question(question_list):
    map_dict = get_map_dict()
    string = ''
    for i in range(len(question_list)):
        string += map_dict[question_list[i]]['question'] + '和'
    string = string.rstrip('和')
    print(string)
