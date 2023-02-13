# -*- coding: utf-8 -*-            
# @Time : 2023/2/12 16:27
# @Author : JinYueYu
# Description : 
# Copyright JinYueYu.All Right Reserved.
import numpy as np
import pandas as pd
from sklearn import tree
from matplotlib import pyplot as plt

plt.rcParams['savefig.dpi'] = 300
plt.rcParams['figure.dpi'] = 300

model = tree.DecisionTreeClassifier()
question_list = ['Q26', 'Q27', 'Q28', 'Q29', 'Q30']
data_path = '../../data/data.xlsx'
data = pd.read_excel(data_path)
x = data[question_list].values
y = data['Q16'].values
model = model.fit(x, y)
y1 = model.predict(x)
score = 1 - np.count_nonzero(y - y1) / len(y)
print(score)
# text_representation = tree.export_text(model)
# print(text_representation)

fig = plt.figure(figsize=(30, 30))
_ = tree.plot_tree(model, max_depth=3, feature_names=question_list, class_names=['1', '2'], filled=True)

# Save picture
fig.savefig("../../pic/tree.png")
