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
    def __init__(self, data_path, question_list):
        self.data = pd.read_excel(data_path)
        self.question_list = question_list
        self.alpha = 0.05
        self.refer = None
        self.decode = Decode(data_path)
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
        if '???' in type:
            self.crosstab = pd.crosstab(self.data[self.question_list[0]],
                                        self.data[self.question_list[1]],
                                        margins=True)
        elif '???' in type:
            string = self.question_list[1]
            dictionary = self.map_dict[string]
            values_list = []
            # ???????????????map_dict????????????,?????????"-3"???????????????
            for i in range(len(dictionary) - 3):
                values_list.append(string + '|' + str(i + 1))
            colnames = list(range(len(dictionary) - 3))
            colnames = [i + 1 for i in colnames]
            # margins?????????Q15???????????
            self.crosstab = pd.pivot_table(self.data, index=self.question_list[0],
                                           values=values_list,
                                           aggfunc=np.sum)
            self.crosstab.columns = colnames
            self.crosstab.columns.name = string
            self.crosstab['All'] = np.sum(self.crosstab, axis=1)
            self.crosstab.loc['All'] = np.sum(self.crosstab, axis=0)
        else:
            raise '?????????Ridit????????????????????????????????????????????????'

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
                # ???????????????????????????
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
        print('?????????????????????????????????:' + str(self.use_combine_as_refer))
        print('???????????????:' + str(self.question_list))
        self.decode.decoding_question(self.question_list)
        if not (self.crosstab['All'][:self.row] >= 43).all():
            warnings.warn('?????????Ridit?????????????????????????????????????????????50???')
        if self.row == 2:
            dev = np.abs(self.crosstab['Ridit'][1] - self.crosstab['Ridit'][2])
            z = dev / np.sqrt(self.crosstab['std'][2] ** 2 / self.crosstab['All'][2] + self.crosstab['std'][1] ** 2 /
                              self.crosstab['All'][1])
            p_value = 1 - norm.cdf(z)
            print('u???????????????:%.3f;p???:%.6f' % (z, p_value))
            if z > norm.ppf(q=1 - self.alpha / 2):
                print('??????????????????')
        else:
            degree_freedom = self.row - 1
            ub = chi2.ppf(q=1 - self.alpha / 2, df=degree_freedom)
            a = self.crosstab['Ridit'][:self.row] - 0.5
            chi_square = (self.row - 1) * (self.col - 1) * np.dot(a * a, self.crosstab['All'][:self.row])
            p_value = 1 - chi2.cdf(chi_square, df=degree_freedom)
            print('?????????????????????:%.3f;?????????:%.1f;p???:%.6f' % (chi_square, degree_freedom, p_value))
            if chi_square > ub:
                print('??????????????????')
                self.decode.decoding_chi2_sig(self.question_list)
        self.ridit_boxplot()
        print(self.crosstab)

    def ridit_boxplot(self):
        print('?????????????????????......')
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
        plt.ylabel('??????Ridit???')
        plt.savefig(f'../../pic/ridit_boxplot/{self.question_list[0]}-{self.question_list[1]}.png')
        # plt.show()

    def k_wboxplot(self):
        warnings.filterwarnings('ignore')
        self.data['rank'] = self.data[self.question_list[1]].rank(method='average', ascending=True)
        x_tick_loc, x_tick_name, rank_list, frequency = list(), list(), list(), list()
        for i in range(self.row):
            x_tick_name.append(self.map_dict[self.question_list[0]][str(i + 1)])

            rank = round(np.mean(self.data[self.data[self.question_list[0]] == i + 1]['rank']), 2)
            slis = self.data[self.data[self.question_list[0]] == i + 1][self.question_list[1]] == 1
            freq = np.sum(slis) / len(slis)
            rank_list.append(rank)
            frequency.append(freq)
        color1 = ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])]
        fig = plt.figure(figsize=(12, 6))
        ax1 = fig.add_subplot(1, 2, 1)
        ax2 = fig.add_subplot(1, 2, 2)
        ax1.bar(x_tick_name, rank_list, edgecolor='k', color=color1)
        for i in range(len(x_tick_name)):
            ax1.text(x=i - 0.05 * self.row, y=rank_list[i] + 0.01 * max(rank_list), s=rank_list[i])
        ax1.set_xticklabels(x_tick_name, rotation=25)
        ax1.set_ylabel('???????????????')

        color2 = ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])]
        ax2.bar(x_tick_name, frequency, edgecolor='k', color=color2)
        for j in range(len(x_tick_name)):
            ax2.text(x=j - 0.05 * self.row, y=frequency[j] + 0.01 * max(frequency),
                     s=str(frequency[j] * 100)[:4] + '%')
        ax2.set_ylabel('??????????????????????????????')
        ax2.set_xticklabels(x_tick_name, rotation=25)
        plt.savefig(f'../../pic/K-Wboxplot/{self.question_list[0]}-{self.question_list[1]}.png')
        # plt.show()
