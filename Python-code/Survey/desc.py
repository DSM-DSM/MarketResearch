# -*- coding: utf-8 -*-            
# @Time : 2023/2/13 14:53
# @Author : JinYueYu
# Description : 
# Copyright JinYueYu.All Right Reserved.
import pandas as pd
import numpy as np
from decode import get_map_dict
import matplotlib.pyplot as plt
import matplotlib


def plot_RAdio(data, labels):
    matplotlib.rcParams['font.family'] = 'SimHei'  # 将字体设置为黑体'SimHei'
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']

    dataLenth = len(labels)  # 数据长度
    angles = np.linspace(0, 2 * np.pi, dataLenth, endpoint=False)  # 根据数据长度平均分割圆周长

    # 闭合
    data = np.concatenate((data, [data[0]]))
    angles = np.concatenate((angles, [angles[0]]))
    labels = np.concatenate((labels, [labels[0]]))  # 对labels进行封闭

    plt.figure(facecolor="white")  # facecolor 设置框体的颜色
    plt.subplot(111, polar=True)  # 将图分成1行1列，画出位置1的图；设置图形为极坐标图
    plt.plot(angles, data, 'go-', linewidth=2)
    plt.fill(angles, data, facecolor='g', alpha=0.25)  # 填充两条线之间的色彩，alpha为透明度
    plt.thetagrids(angles * 180 / np.pi, labels)  # 做标签
    # plt.figtext(0.52,0.95,'雷达图',ha='center')   #添加雷达图标题
    plt.grid(True)
    plt.show()


data_path = '../data_ridit.xlsx'
data = pd.read_excel(data_path)
map = get_map_dict(data_path)
save_to = '../desc.xlsx'
with pd.ExcelWriter(save_to) as xlsx:
    for i in range(len(map)):
        ques = 'Q' + str(i + 1)
        if '矩阵' in map[ques]['question_type']:
            dict = map[ques]
            value_list = [f'{ques}|R{j + 1}' for j in range(len(dict) - 3)]
            meaning_list = [dict[f'R{k + 1}'] for k in range(len(dict) - 3)]
            desc = data[value_list].describe()
            desc.columns = meaning_list
            desc.loc['mean_rank', :] = desc.loc['mean', :].rank(method='min', ascending=False)
            # plot_RAdio(desc.loc['mean', :], meaning_list)
            desc.to_excel(xlsx, sheet_name=ques)
