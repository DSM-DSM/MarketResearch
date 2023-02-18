# -*- coding: utf-8 -*-            
# @Time : 2023/2/9 15:01
# @Author : JinYueYu
# Description : 
# Copyright JinYueYu.All Right Reserved.
import pandas as pd
import csv
import numpy as np
from decode import get_map_dict

data = pd.read_excel('../data_ridit.xlsx', sheet_name='Sheet1')
map = get_map_dict('../data_ridit.xlsx')
# 统计对单身经济的态度
data['Q5'].value_counts()
data.set_index('答题序号', inplace=True)
# kmodes分块数据
Kmodes_list = ['Q26', 'Q27', 'Q28', 'Q29', 'Q30']
# data[Kmodes_list].to_excel('../data_kmodes.xlsx', index=True)
# Kruskal-Willis检验数据
for i in range(len(Kmodes_list)):
    with open(f"../../市场调查/data/{Kmodes_list[i]} K-Wtest.csv", "w") as csvfile:
        writer = csv.writer(csvfile)
        for j in range(len(map[Kmodes_list[i]]) - 3):
            writer.writerow(data[data[Kmodes_list[i]] == j + 1]['Q16'])

# 删除csv空行
# data = pd.read_csv("monitor.csv")
# res = data.dropna(how="all")
# res.to_csv("monitor1.csv", index=False)

