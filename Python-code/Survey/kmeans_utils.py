# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from scipy.spatial.distance import hamming


def init_centroids(x, k):
    """
    初始化K个质心
    质心应该从数据集样本中随机选取
    输入
        x：数据集
        k：质心数
    输出
        centroids：初始化的质心
    """
    # 随机置乱数据集
    rand_idx = np.random.permutation(len(x))
    # 前k个样本作为质心
    centroids = x[rand_idx[:k]]
    return centroids


def e_step(x, centroids):
    """
    计算每个样本离质心的距离
    返回X数据集中离centroids最近的质心索引
    """
    # 返回值
    r = np.zeros(len(x), dtype=np.int)
    j_value = 0

    for ii in range(len(x)):
        dist_c = list()
        for jj in range(centroids.shape[0]):
            dist_c.append(hamming(x[ii], centroids[jj]))
        dist_c = np.array(dist_c)
        r[ii] = np.argmin(dist_c)
        j_value += np.min(dist_c)

    return r, j_value


def m_step(x, r, k):
    """
    计算指派每个旧质心的样本的均值，返回新质心
    输入
        x：数据集
        r：数据集中每个样本指派给旧质心的索引。每个元素取值为[1..K]
        k：质心的个数
    输出
        centroids：计算得到的新质心
    """
    # 初始化返回值
    centroids = np.zeros((k, len(x[0])))

    # 求均值
    for i in range(k):
        # 簇i的全部样本
        sub_x = pd.DataFrame(x[np.where(r == i)])
        # 使用一个簇的每个属性出现频率最大的那个属性值作为代表簇的属性值
        new_centriod = list()
        for j in range(len(x[0])):
            new_centriod.append(sub_x[j].value_counts().idxmax())
        centroids[i] = np.array(new_centriod)
    return centroids
