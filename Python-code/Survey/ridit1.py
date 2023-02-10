# -*- coding: utf-8 -*-            
# @Time : 2023/2/9 15:33
# @Author : JinYueYu
# Description : 
# Copyright JinYueYu.All Right Reserved.
import pandas as pd
import numpy as np
from scipy.stats import norm, chi2
from decode import decoding_question


def calculate_stander_ri(crosstab):
    """
    计算标准Ri
    :param crosstab: 交叉列联表
    :return:
    """
    if determine_refer(crosstab):
        k = 'All'
        crosstab.loc['cusum'] = np.cumsum(crosstab.loc['All', :])
        total = crosstab.loc['All', 'All']
        crosstab.loc['All', 'All'] = 0
    else:
        crosstab.loc['All', 'All'] = 0
        k = crosstab[crosstab['All'] == crosstab['All'].max()].index[0]
        crosstab.loc['cusum'] = np.cumsum(crosstab.loc[k, :])
        total = crosstab.loc[k, 'All']
    crosstab.loc['Ri'] = 0
    for i in range(crosstab.shape[1] - 1):
        if i == 0:
            crosstab.iloc[4, i] = (crosstab.loc[k, :][i + 1] * 0.5) / total
        else:
            crosstab.iloc[4, i] = (crosstab.loc[k, :][i + 1] * 0.5 + crosstab.iloc[3, i - 1]) / total
    return crosstab, k, total


def calculate_std(crosstab, k):
    crosstab['std'] = 0
    if determine_refer(crosstab):
        for i in range(crosstab.shape[0] - 3):
            crosstab['std'][i] = calculate_std2(crosstab, k)
    else:
        for i in range(crosstab.shape[0] - 3):
            k = crosstab.iloc[i, :].name
            crosstab['std'][i] = calculate_std2(crosstab, k)
    return crosstab


def calculate_std2(crosstab, k):
    total = crosstab.loc[k, 'All']
    Ri_square = crosstab.loc['Ri', :] * crosstab.loc['Ri', :]
    expectacy = np.dot(crosstab.loc['Ri', :], crosstab.loc[k, :])
    var = (np.dot(Ri_square, crosstab.loc[k, :]) - (expectacy ** 2) / total) / (total - 1)
    std = np.sqrt(var)
    return std


def calculate_each_ridit(crosstab):
    """
    计算每组的Ridit值
    :param crosstab:
    :param k: 参照组的标号
    :param total: 参照组总个数
    :return:
    """
    crosstab.loc['cusum', 'All'] = 0
    crosstab['Ridit'] = 0
    for i in range(crosstab.shape[0] - 3):
        crosstab.loc[i + 1, 'Ridit'] = (np.dot(crosstab.iloc[i, :], crosstab.iloc[4, :])) / crosstab.loc[i + 1, 'All']
    return crosstab


def ridit_test(crosstab, k, question_list):
    alpha = 0.05
    if crosstab.shape[0] - 3 == 2:
        std = crosstab.loc[k, 'std']
        decoding_question(question_list)
        dev = np.abs(crosstab['Ridit'][1] - crosstab['Ridit'][2])
        z = dev / (std * np.sqrt(1 / crosstab['All'][2] + 1 / crosstab['All'][1]))
        p_value = 1 - norm.cdf(z)
        print('u检验统计量:%.3f;p值:%.6f' % (z, p_value))
        if z > norm.ppf(q=1 - alpha / 2):
            print('有显著差异！')
    else:
        decoding_question(question_list)
        degree_freedom = crosstab.shape[0] - 4
        ub = chi2.ppf(q=1 - alpha / 2, df=degree_freedom)
        a = (crosstab['Ridit'][:degree_freedom + 1] - 0.5) * (crosstab['Ridit'][:degree_freedom + 1] - 0.5)
        chi_square = (crosstab.shape[0] - 4) * (crosstab.shape[1] - 3) * np.dot(a, crosstab['All'][:degree_freedom + 1])
        p_value = 1 - chi2.cdf(chi_square, df=degree_freedom)
        print(p_value)
        print('卡方检验统计量:%.3f;自由度:%.1f;p值:%.6f' % (chi_square, degree_freedom, p_value))
        if chi_square > ub:
            print('有显著差异！')


def main():
    data = pd.read_excel('../../data/data.xlsx')
    question_list = ['Q27', 'Q1']
    ridit = Ridit(data, question_list)


if __name__ == '__main__':
    main()


