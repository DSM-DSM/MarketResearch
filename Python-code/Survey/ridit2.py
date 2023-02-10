# -*- coding: utf-8 -*-            
# @Time : 2023/2/10 17:47
# @Author : JinYueYu
# Description : 
# Copyright JinYueYu.All Right Reserved.
import pandas as pd
import numpy as np
from scipy.stats import norm, chi2
from decode import decoding_question


class Ridit():
    def __init__(self, data, question_list):
        self.alpha = 0.05
        self.refer = None
        self.refer_total = None
        self.use_combine_as_refer = None
        self.question_list = question_list
        self.crosstab = pd.crosstab(data[question_list[0]], data[question_list[1]], margins=True)
        self.row = self.crosstab.shape[0] - 1
        self.col = self.crosstab.shape[1] - 1
        self.determine_refer()

    def determine_refer(self):
        self.use_combine_as_refer = True
        if 0.5 <= self.crosstab['All'].max() / self.crosstab['All'].min() <= 2:
            self.use_combine_as_refer = False

    def calculate_stander_ri(self):
        if self.use_combine_as_refer:
            self.refer = 'All'
            self.crosstab.loc['cusum'] = np.cumsum(self.crosstab.loc[self.refer, :])
            self.refer_total = max(self.crosstab.loc[self.refer])
            self.crosstab.loc['All', 'All'] = 0
        else:
            self.crosstab.loc['All', 'All'] = 0
            self.refer = self.crosstab[self.crosstab['All'] == self.crosstab['All'].max()].index[0]
            self.crosstab.loc['cusum'] = np.cumsum(self.crosstab.loc[self.refer, :])
            self.refer_total = self.crosstab.loc[self.refer, 'All']
        self.crosstab.loc['Ri'] = 0.
        self.crosstab.loc['cusum']['All'] = 0
        for i in range(self.crosstab.shape[1] - 1):
            if i == 0:
                # 需要保证都是升序！
                self.crosstab.loc['Ri', i + 1] = self.crosstab.loc[self.refer, :][i + 1] / self.refer_total / 2
            else:
                self.crosstab.loc['Ri', i + 1] = (self.crosstab.loc[self.refer, :][i + 1] * 0.5 + self.crosstab.loc[
                    'cusum', i]) / self.refer_total

    def calculate_std(self):
        self.crosstab['std'] = 0
        if self.use_combine_as_refer:
            for i in range(self.row):
                self.crosstab.loc[i + 1, 'std'] = self.calculate_std2(self.refer)
        else:
            for i in range(self.row):
                row_key = self.crosstab.iloc[i, :].name
                self.crosstab.loc[i + 1, 'std'] = self.calculate_std2(row_key)

    def calculate_std2(self, row_key):
        total = self.crosstab.loc[row_key, 'All']
        if row_key == 'All':
            total = self.refer_total
        Ri_square = self.crosstab.loc['Ri', :] * self.crosstab.loc['Ri', :]
        expectacy = np.dot(self.crosstab.loc['Ri', :], self.crosstab.loc[row_key, :])
        var = (np.dot(Ri_square, self.crosstab.loc[row_key, :]) - (expectacy ** 2) / total) / (total - 1)
        std = np.sqrt(var)
        return std

    def calculate_each_ridit(self):
        self.crosstab['Ridit'] = 0
        for i in range(self.row):
            ridit_i = np.dot(self.crosstab.loc[i + 1, :], self.crosstab.loc['Ri', :])
            self.crosstab.loc[i + 1, 'Ridit'] = ridit_i / self.crosstab.loc[i + 1, 'All']

    def ridit_test(self):
        if self.row == 2:
            decoding_question(question_list)
            dev = np.abs(self.crosstab['Ridit'][1] - self.crosstab['Ridit'][2])
            z = dev / np.sqrt(self.crosstab['std'][2] ** 2 / self.crosstab['All'][2] + self.crosstab['std'][1] ** 2 /
                              self.crosstab['All'][1])
            p_value = 1 - norm.cdf(z)
            print('u检验统计量:%.3f;p值:%.6f' % (z, p_value))
            if z > norm.ppf(q=1 - self.alpha / 2):
                print('有显著差异！')
        else:
            decoding_question(question_list)
            degree_freedom = self.row - 1
            ub = chi2.ppf(q=1 - self.alpha / 2, df=degree_freedom)
            a = self.crosstab['Ridit'][:self.row] - 0.5
            chi_square = (self.row - 1) * (self.col - 1) * np.dot(a * a, self.crosstab['All'][:self.row])
            p_value = 1 - chi2.cdf(chi_square, df=degree_freedom)
            print('卡方检验统计量:%.3f;自由度:%.1f;p值:%.6f' % (chi_square, degree_freedom, p_value))
            if chi_square > ub:
                print('有显著差异！')


data = pd.read_excel('../../data/data.xlsx')
question_list = ['Q27', 'Q1']
ridit = Ridit(data, question_list)
ridit.calculate_stander_ri()
ridit.calculate_std()
ridit.calculate_each_ridit()
ridit.ridit_test()
print(ridit.crosstab)
