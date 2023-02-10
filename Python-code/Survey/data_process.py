# -*- coding: utf-8 -*-            
# @Time : 2023/2/9 15:01
# @Author : JinYueYu
# Description : 
# Copyright JinYueYu.All Right Reserved.
import pandas as pd
import numpy as np

data = pd.read_excel('../../data/data.xlsx', sheet_name='Sheet1')
# 统计对单身经济的态度
data['Q5'].value_counts()
data.set_index('答题序号', inplace=True)
# kmodes分块数据
Kmodes_list = ['Q26', 'Q27', 'Q28', 'Q29', 'Q30']
data[Kmodes_list].to_excel('../data_Q26-30.xlsx', index=True)

