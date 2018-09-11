import pandas as pd

from common_utils import *

"""
01EPS|02近四季EPS|03每股淨值|04毛利率|05營業利益率|06ROE|07近四季ROE|08單季營收季增率|09單季營收年增率|10近4季營收季增率|11近4季營收年增率|
12單季毛利季增率|13單季毛利年增率|14近4季毛利季增率|15近4季毛利年增率|16單季營業利益季增率|17單季營業利益年增率|18近4季營業利益季增率|19近4季營業利益年增率|
20單季EPS季增率|21單季EPS年增率|22近4季EPS季增率|23近4季EPS年增率, 共138欄位
"""
df = pd.read_csv('dog.csv', header=None, index_col=0, na_values=['負','負轉正','無','前期為零'])
df2 = df.astype(float)
#print(df2.shape)

"""
01前年度月|02前年度營收|03前年度年增率|04今年度月|05今年度營收|06今年度年增率|07今年度累計營收|08今年度累積營收年增率|09達成率
一共9個欄位 12個月就有108個欄位
"""
df3 = pd.read_csv('revenue.csv', header=None, index_col=0, na_values=['-'])
df4 = df3.astype(float)
#print(df4.shape)


df5 = pd.concat([df2,df4],axis=1,ignore_index=True)
#print(df5.shape)
#print(df5.columns.tolist())

offset1 = -1 - 6 # -1是column index從0開始 -6是讓width的乘數可以直接使用欄位號碼
width1 = 6 # 201701~201802 共6季
offset2 = 138 - 1 - 9 # dog營收欄位共138個 -1是column index從0開始 -9是讓width2的乘數可以直接使用月份
width2 = 9 # yahoo營收欄位共9個

# ============================================================

# 挑 201801 ROE > 1% 且 201802 ROE > 1% 且 六月營收年增率 > 20% 且 七月營收年增率 > 20% 的股票
selectedList = df5[(df5[6*width1+5+offset1] > 1) & (df5[6*width1+6+offset1] > 1) & (df5[6+width2*6+offset2] > 20) & (df5[6+width2*7+offset2] > 20)].index.tolist()

# ============================================================

companyMap = getCompanyMap()
outList = []
for item in selectedList:
	companyName = companyMap[str(item)].name
	fullName = '{}({})'.format(item,companyName)
	outList.append(fullName)
	print(fullName, end=' ')

writeToFile = True
count = 0
if(writeToFile):
	with open('selected.txt', 'w', encoding='utf-8') as f:
		for item in outList:
			f.write("%s," % item)
			count = count + 1 
			if(count % 10 == 0):
				f.write("\n")
				
