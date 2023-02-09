# -*- coding: utf-8 -*-            
# @Time : 2023/2/9 15:33
# @Author : JinYueYu
# Description : 
# Copyright JinYueYu.All Right Reserved.
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

data = pd.read_excel('../../data/data.xlsx', sheet_name='Sheet1')
model = KMeans(n_clusters=3)
