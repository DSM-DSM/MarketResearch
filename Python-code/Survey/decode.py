# -*- coding: utf-8 -*-            
# @Time : 2023/2/9 23:00
# @Author : JinYueYu
# Description : 
# Copyright JinYueYu.All Right Reserved.
import pandas as pd
import numpy as np

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
final_map = []
for key, group in groups:
    print(key)
    print(group)
