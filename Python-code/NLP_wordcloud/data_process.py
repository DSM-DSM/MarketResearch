# -*- coding: utf-8 -*-            
# @Time : 2023/1/1 16:49
# @Author : JinYueYu
# Description : 
# Copyright JinYueYu.All Right Reserved.
import pandas as pd

_MAPPING = (
    u'零', u'一', u'二', u'三', u'四', u'五', u'六', u'七', u'八', u'九', u'十', u'十一', u'十二', u'十三', u'十四',
    u'十五', u'十六', u'十七', u'十八', u'十九')
_P0 = (u'', u'十', u'百', u'千',)
_S4 = 10 ** 4


def _to_chinese4(num):
    assert (0 <= num and num < _S4)
    if num < 20:
        return _MAPPING[num]
    else:
        lst = []
        while num >= 10:
            lst.append(num % 10)
            num = num / 10
        lst.append(num)
        c = len(lst)  # 位数
        result = u''

        for idx, val in enumerate(lst):
            val = int(val)
            if val != 0:
                result += _P0[idx] + _MAPPING[val]
                if idx < c - 1 and lst[idx + 1] == 0:
                    result += u'零'
        return result[::-1]


def filter(df):
    df.dropna(inplace=True)
    df.drop_duplicates(subset=['标题', 'short'], keep='first', inplace=True)
    drop_list = []
    df.reset_index(inplace=True)
    for i in range(df.shape[0]):
        if not df.iloc[i, :].short:
            drop_list.append(i)
        if type(df.iloc[i, :].short) != str:
            drop_list.append(i)
    df.drop(drop_list, inplace=True)
    return df


# df = pd.DataFrame()
# for i in range(10):
#     num = _to_chinese4(i + 1)
#     path = f'../data/孤独的美食家第{num}季短评.xlsx'
#     df_1 = pd.read_excel(path)
#     df_1['season'] = i
#     df_1 = filter(df_1)
#     df = pd.concat([df, df_1])
# print(df.shape)
# df.reset_index(inplace=True)
# df.to_excel('../data/孤独的美食家十季度短评处理后.xlsx')

df_1 = pd.read_excel('../../data/背景/深夜食堂日版时序.xlsx')
df_2 = pd.read_excel('../../data/背景/深夜食堂日版热评.xlsx')
df_1 = filter(df_1)
df_2 = filter(df_2)
df_1 = pd.concat([df_1, df_2])
df_1.reset_index(inplace=True)
df_1.to_excel('../data/背景/合并版.xlsx')
