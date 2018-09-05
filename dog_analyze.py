import pandas as pd

"""
01EPS|02近四季EPS|03每股淨值|04毛利率|05營業利益率|06ROE|07近四季ROE|08單季營收季增率|09單季營收年增率|10近4季營收季增率|11近4季營收年增率|
12單季毛利季增率|13單季毛利年增率|14近4季毛利季增率|15近4季毛利年增率|16單季營業利益季增率|17單季營業利益年增率|18近4季營業利益季增率|19近4季營業利益年增率|
20單季EPS季增率|21單季EPS年增率|22近4季EPS季增率|23近4季EPS年增率, 共138欄位
"""
df = pd.read_csv('dog.csv', header=None, index_col=0, na_values=['負','負轉正','無','前期為零'])
df2 = df.astype(float)
print(df2.shape)


# 挑201801單季毛利年增率 > 20%的股票 且 201802單季毛利年增率 > 20%的股票
selectedList = df2[(df2[12*6+5] > 20) & (df2[12*6+6] > 20)].index.tolist()
print(selectedList)

"""
01前年度月|02前年度營收|03前年度年增率|04今年度月|05今年度營收|06今年度年增率|07今年度累計營收|08今年度累積營收年增率|09達成率
一共9個欄位 12個月就有108個欄位
"""
df3 = pd.read_csv('revenue.csv', header=None, index_col=0)
df4 = df3.astype(float)
print(df4.shape)


df5 = pd.concat([df2,df4],axis=1,ignore_index=True)
print(df5.shape)
print(df5.columns.tolist())

# 挑201801單季毛利年增率 > 150%的股票 且 201802單季毛利年增率 > 200%的股票 且 六月累積營收年增率 > 60%的股票 且 挑七月累積營收年增率 > 40%的股票
offset = 137
selectedList = df5[(df5[12*6+5-1] > 150) & (df5[12*6+6-1] > 200) & (df5[8+9*5+offset] > 60) & (df5[8+9*6+offset] > 40)].index.tolist()
print(selectedList)

