# -*- coding: utf-8 -*-
# @Time : 2023/2/11 14:47
# @Author : JinYueYu
# Description : 
# Copyright JinYueYu.All Right Reserved.
import pandas as pd
from ridit import Ridit


def main():
    data_path = '../../data/data.xlsx'
    # data_path = '../../data/data.xlsx'
    # 第一个问题必须为检验的指标，第二个问题必须为等级指标
    list_1 = ['Q26', 'Q27', 'Q28', 'Q29', 'Q30']
    for i in range(len(list_1)):
        question_list = [list_1[i], 'Q16']
        ridit = Ridit(data_path, question_list)
        # ridit.calculate_stander_ri()
        # ridit.calculate_std()
        # ridit.calculate_each_ridit()
        # ridit.calculate_ci()
        # ridit.ridit_test()
        ridit.k_wboxplot()


if __name__ == '__main__':
    main()
