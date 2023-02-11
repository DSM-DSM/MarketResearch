# -*- coding: utf-8 -*-            
# @Time : 2023/2/9 23:00
# @Author : JinYueYu
# Description : 
# Copyright JinYueYu.All Right Reserved.
import warnings
import pandas as pd
import numpy as np


def get_map_dict():
    """
    特别说明question_order各取值的含义：
    1.态度类问题：利于主题的为优，反之亦然；
    2.频率&价格类问题：频率&价格高的为优，反之亦然；
    3.测谎类问题及其他：仅取值为“无”；
    :return:
    """
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
        single_question['question_order'] = group.iloc[1, 2]
        for i in range(group.shape[0] - 2):
            single_question[group.iloc[i + 2, 1]] = group.iloc[i + 2, 2]
        map_dict[key] = single_question
    return map_dict


class Decode():
    def __init__(self):
        self.map_dict = get_map_dict()

    def decoding_centroids(self, question, coder):
        coder = coder.astype(int)
        if len(coder) != len(question):
            import warnings
            warnings.warn('输入长度不一致！！')
            return
        else:
            string = str()
            for i in range(len(coder)):
                string += self.map_dict[question[i]][str(coder[i])] + ','
            string = string.rstrip(',')
            print(string)

    def decoding_question(self, question_list):
        string = ''
        for i in range(len(question_list)):
            string += self.map_dict[question_list[i]]['question'] + '和'
        string = string.rstrip('和')
        print(string)

    def decoding_chi2_sig(self, question_list):
        if len(question_list) > 2:
            warnings.warn('错误，Ridit检验问题数量大于2！')
            return
        ques_ord = self.map_dict[question_list[0]]['question_order'] + self.map_dict[question_list[1]]['question_order']
        if '优' not in ques_ord:
            warnings.warn('错误，不包含能够进行Ridit检验的对象！')
            return
        if '优劣' in ques_ord:
            print('检验问题等级排序为：先优后劣，平均Ridit值越小越好。')
        else:
            print('检验问题等级排序为：先劣后优，平均Ridit值越大越好。')

