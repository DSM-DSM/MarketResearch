# -*- coding: utf-8 -*-            
# @Time : 2023/2/10 17:47
# @Author : JinYueYu
# Description : 
# Copyright JinYueYu.All Right Reserved.
import re
import warnings
import random
import colorsys
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np
from scipy.stats import norm, chi2
from decode import Decode

mpl.rcParams['font.sans-serif'] = ['simhei']
mpl.rcParams['axes.unicode_minus'] = False
plt.rcParams['savefig.dpi'] = 200
plt.rcParams['figure.dpi'] = 200


def ncolors(num):
    rgb_colors = []
    if num < 1:
        return rgb_colors
    hls_colors = get_n_hls_colors(num)
    for hlsc in hls_colors:
        _r, _g, _b = colorsys.hls_to_rgb(hlsc[0], hlsc[1], hlsc[2])
        r, g, b = [int(x * 255.0) for x in (_r, _g, _b)]
        rgb_colors.append([r, g, b])

    return rgb_colors


def get_n_hls_colors(num):
    hls_colors = []
    i = 0
    step = 360.0 / num
    while i < 360:
        h = i
        s = 90 + random.random() * 10
        l = 50 + random.random() * 10
        _hlsc = [h / 360.0, l / 100.0, s / 100.0]
        hls_colors.append(_hlsc)
        i += step

    return hls_colors


def color(value):
    digit = list(map(str, range(10))) + list("ABCDEF")
    if isinstance(value, tuple):
        string = '#'
        for i in value:
            a1 = i // 16
            a2 = i % 16
            string += digit[a1] + digit[a2]
        return string
    elif isinstance(value, str):
        a1 = digit.index(value[1]) * 16 + digit.index(value[2])
        a2 = digit.index(value[3]) * 16 + digit.index(value[4])
        a3 = digit.index(value[5]) * 16 + digit.index(value[6])
        return (a1, a2, a3)


class Ridit():
    def __init__(self, data, question_list):
        self.data = data
        self.question_list = question_list
        self.alpha = 0.05
        self.refer = None
        self.decode = Decode()
        self.map_dict = self.decode.map_dict
        self.crosstab = None
        self.init_crosstab()
        self.refer_total = None
        self.use_combine_as_refer = True
        self.determine_refer()
        self.row = self.crosstab.shape[0] - 1
        self.col = self.crosstab.shape[1] - 1

    def init_crosstab(self):
        type = self.map_dict[self.question_list[1]]['question_type']
        if '单' in type:
            self.crosstab = pd.crosstab(self.data[self.question_list[0]],
                                        self.data[self.question_list[1]],
                                        margins=True)
        elif '多' in type:
            string = self.question_list[1]
            dictionary = self.map_dict[string]
            values_list = []
            # 后期若增加map_dict中的属性,此处的"-3"需要调整！
            for i in range(len(dictionary) - 3):
                values_list.append(string + '|' + str(i + 1))
            colnames = list(range(len(dictionary) - 3))
            colnames = [i + 1 for i in colnames]
            self.crosstab = pd.pivot_table(self.data, index=self.question_list[0],
                                           values=values_list,
                                           aggfunc=np.sum,
                                           margins=True)
            self.crosstab.columns = colnames
            self.crosstab.columns.name = string
            self.crosstab['All'] = np.sum(self.crosstab, axis=1)
        else:
            raise '错误，Ridit检验出现单选多选以外的等级指标。'

    def determine_refer(self):
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
                self.crosstab.loc[i + 1, 'std'] = self.__calculate_std2(self.refer)
        else:
            for i in range(self.row):
                row_key = self.crosstab.iloc[i, :].name
                self.crosstab.loc[i + 1, 'std'] = self.__calculate_std2(row_key)

    def __calculate_std2(self, row_key):
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

    def calculate_ci(self):
        self.crosstab['ci_l'] = self.crosstab['Ridit'] - self.crosstab['std'] / self.crosstab['All'] ** 0.5
        self.crosstab['ci_u'] = self.crosstab['Ridit'] + self.crosstab['std'] / self.crosstab['All'] ** 0.5
        self.crosstab.fillna(0, inplace=True)

    def ridit_test(self):
        print('是否将合并组作为参照组:' + str(self.use_combine_as_refer))
        print('检验的问题:' + str(self.question_list))
        self.decode.decoding_question(self.question_list)
        if not (self.crosstab['All'] > 50).all():
            warnings.warn('错误，Ridit检验要求每一组的样本个数至少为50。')
        if self.row == 2:
            dev = np.abs(self.crosstab['Ridit'][1] - self.crosstab['Ridit'][2])
            z = dev / np.sqrt(self.crosstab['std'][2] ** 2 / self.crosstab['All'][2] + self.crosstab['std'][1] ** 2 /
                              self.crosstab['All'][1])
            p_value = 1 - norm.cdf(z)
            print('u检验统计量:%.3f;p值:%.6f' % (z, p_value))
            if z > norm.ppf(q=1 - self.alpha / 2):
                print('有显著差异！')
        else:
            degree_freedom = self.row - 1
            ub = chi2.ppf(q=1 - self.alpha / 2, df=degree_freedom)
            a = self.crosstab['Ridit'][:self.row] - 0.5
            chi_square = (self.row - 1) * (self.col - 1) * np.dot(a * a, self.crosstab['All'][:self.row])
            p_value = 1 - chi2.cdf(chi_square, df=degree_freedom)
            print('卡方检验统计量:%.3f;自由度:%.1f;p值:%.6f' % (chi_square, degree_freedom, p_value))
            if chi_square > ub:
                print('有显著差异！')
                self.decode.decoding_chi2_sig(self.question_list)
        self.boxplot()
        print(self.crosstab)

    def boxplot(self):
        print('开始绘制箱线图......')
        plt.figure(figsize=(6, 8))
        c_list = list(map(lambda x: color(tuple(x)), ncolors(self.row)))
        ruler = 1 / (self.row + 1)
        line_length = ruler * 0.3
        x_tick_loc, x_tick_name = list(), list()
        for i in range(self.row):
            x = ruler * (i + 1)
            x_tick_loc.append(x)
            x_tick_name.append(self.map_dict[self.question_list[0]][str(i + 1)])
            plt.plot(x, self.crosstab['Ridit'][i + 1], marker='o', markersize=5, c=c_list[i])
            plt.axhline(self.crosstab['ci_l'][i + 1], x - line_length, x + line_length, c=c_list[i])
            plt.axhline(self.crosstab['ci_u'][i + 1], x - line_length, x + line_length, c=c_list[i])
        plt.grid()
        plt.xticks(x_tick_loc, x_tick_name, rotation=23)
        plt.xlim(0, 1)
        string1 = self.map_dict[self.question_list[0]]['question']
        string1 = re.sub(r'[^\u4e00-\u9fa5]', '', string1)
        string2 = self.map_dict[self.question_list[1]]['question']
        string2 = re.sub(r'[^\u4e00-\u9fa5]', '', string2)
        plt.xlabel(str(self.question_list[0]) + ':' + string1 + '\n' +
                   str(self.question_list[1]) + ':' + string2)
        plt.ylabel('平均Ridit值')
        plt.savefig(f'../../pic/ridit_boxplot/{self.question_list[0]}-{self.question_list[1]}.png')
        plt.show()
