# -*- coding: utf-8 -*-            
# @Time : 2023/2/11 14:47
# @Author : JinYueYu
# Description : 
# Copyright JinYueYu.All Right Reserved.
import pandas as pd
from ridit import Ridit


def main():
    data = pd.read_excel('../../data/data.xlsx')
    # 第一个问题必须为检验的指标，第二个问题必须为等级指标
    question_list = ['Q28', 'Q4']
    ridit = Ridit(data, question_list)
    ridit.calculate_stander_ri()
    ridit.calculate_std()
    ridit.calculate_each_ridit()
    ridit.calculate_ci()
    ridit.ridit_test()


if __name__ == '__main__':
    main()
