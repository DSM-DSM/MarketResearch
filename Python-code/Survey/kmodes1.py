# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import kmeans_utils
from decode import Decode

# 防止plt汉字乱码
mpl.rcParams['font.sans-serif'] = ['simhei']
mpl.rcParams['axes.unicode_minus'] = False
plt.rcParams['savefig.dpi'] = 200
plt.rcParams['figure.dpi'] = 200


def plot_jhistory(j_history):
    """
    绘制代价J的下降曲线
    输入参数：
        Jhistory：J历史
    返回：
        无
    """
    plt.figure()
    plt.plot(np.arange(1, len(j_history) + 1), j_history, 'b-')  # 绘制J历史曲线
    plt.xlabel(u'迭代次数')
    plt.ylabel(u'代价J')
    plt.title(u'J历史')
    plt.savefig('../../pic/kmodes/j_history.png')
    plt.show()


def main():
    # K-Means聚类
    print('\n即将运行K-Means聚类算法。\n\n')
    question = ['Q26', 'Q27', 'Q28', 'Q29', 'Q30']
    # 随机生成样本集
    # np.random.seed(12783)
    data_path = '../data_kmodes.xlsx'
    data = pd.read_excel(data_path)
    data = data[data['Q16'] == 1][['答题序号', 'Q26', 'Q27', 'Q28', 'Q29', 'Q30']]
    decode = Decode(data_path)
    data.set_index('答题序号', inplace=True)
    x = data.values
    # 运行K-Means算法所需参数。可尝试更改这些参数并观察其影响
    k = 10
    max_iters = 8

    # 随机选择初始质心
    initial_centroids = kmeans_utils.init_centroids(x, k)
    print('初始质心:')
    print(initial_centroids[0])
    # 固定选择初始质心
    # initial_centroids = np.array([[5, -1], [0, 6]])

    j_values = np.zeros(max_iters)

    # 保存质心历史
    centroids = np.zeros((max_iters + 1, k, len(x[0])))
    centroids[0] = initial_centroids

    # 迭代运行K-Means算法
    for i in range(max_iters):
        # 输出迭代次数
        print('K-Means迭代次数：%d/%d...\n' % (i + 1, max_iters))

        # 将数据集中的每一个样本分配给离它最近的质心
        r, j_values[i] = kmeans_utils.e_step(x, centroids[i])
        # 计算新质心
        centroids[i + 1] = kmeans_utils.m_step(x, r, k)

    # 绘制J历史轨迹
    plot_jhistory(j_values)
    print('\nK-Means运行完毕。\n\n')
    data[f'class'] = r
    data.to_excel('../kmodes_result.xlsx', index=True)
    print('输出聚类中心具体含义:')
    for i in range(centroids[-1].shape[0]):
        decode.decoding_centroids(question, centroids[-1][i, :])


if __name__ == "__main__":
    main()
