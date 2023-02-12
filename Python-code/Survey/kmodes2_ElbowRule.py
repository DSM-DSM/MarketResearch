# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import kmeans_utils

# 防止plt汉字乱码
mpl.rcParams['font.sans-serif'] = ['simhei']
mpl.rcParams['axes.unicode_minus'] = False
plt.rcParams['savefig.dpi'] = 200
plt.rcParams['figure.dpi'] = 200


def plot_kj(kj):
    """
    绘制KJ关系轨迹
    """
    plt.figure()
    plt.plot(np.arange(1, len(kj) + 1), kj, 'b-')
    plt.xlabel('K')
    plt.ylabel('J')
    plt.title(u'K-J关系轨迹')
    # plt.xlim([1, len(kj)])
    plt.savefig('../../pic/kmodes/K-J.png')
    plt.show()


def main():
    # K-Means聚类
    print('\n即将运行K-Means聚类算法。\n\n')

    # 随机生成样本集
    data_path = '../data_kmodes.xlsx'
    data = pd.read_excel(data_path)
    data.set_index('答题序号', inplace=True)
    x = data.values

    # 运行K-Means算法所需参数。可尝试更改这些参数并观察其影响
    max_iters = 5
    max_k = 10
    kj = np.zeros(max_k)

    # 迭代运行K-Means算法
    for k in range(1, max_k + 1):
        # 随机选择初始质心
        initial_centroids = kmeans_utils.init_centroids(x, k)
        print('初始质心:')
        print(initial_centroids)
        j_values = np.zeros(max_iters)

        # 运行K-Modes算法
        # 保存质心
        centroids = initial_centroids
        for i in range(max_iters):
            # 输出迭代次数
            print('K-Means迭代次数：%d/%d...\n' % (i + 1, max_iters))

            # 将数据集中的每一个样本分配给离它最近的质心
            r, j_values[i] = kmeans_utils.e_step(x, centroids)
            # 计算新质心
            centroids = kmeans_utils.m_step(x, r, k)
            # 如果J不再变化，可以认为已经收敛，退出循环
            if i != 1 and j_values[i] == j_values[i - 1]:
                print(f'已经收敛，迭代次数：{i}\n\n')
                j_values[-1] = j_values[i]
                break
        kj[k - 1] = j_values[-1]

    # 绘制KJ历史轨迹
    plot_kj(kj)
    print('\nK-Means运行完毕。\n\n')


if __name__ == "__main__":
    main()
