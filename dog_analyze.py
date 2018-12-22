import pandas as pd

from common_utils import *

companyMap = getCompanyMap()

# 可調整的參數
dogFieldNum = 23
curSeasonNum = 7
curMonthNum = 11
combinedFieldNum = (dogFieldNum * curSeasonNum) + 108 + 1


"""
01EPS|02近四季EPS|03每股淨值|04毛利率|05營業利益率|06ROE|07近四季ROE|08單季營收季增率|09單季營收年增率|10近4季營收季增率|11近4季營收年增率|
12單季毛利季增率|13單季毛利年增率|14近4季毛利季增率|15近4季毛利年增率|16單季營業利益季增率|17單季營業利益年增率|18近4季營業利益季增率|19近4季營業利益年增率|
20單季EPS季增率|21單季EPS年增率|22近4季EPS季增率|23近4季EPS年增率
共 dogFieldNum * curSeasonNum 欄位
"""
df1 = pd.read_csv('dog.csv', header=None, index_col=0, na_values=['負','負轉正','無','前期為零'])
df1 = df1.astype(float)
#print(df1.shape)

"""
01前年度月|02前年度營收|03前年度年增率|04今年度月|05今年度營收|06今年度年增率|07今年度累計營收|08今年度累積營收年增率|09達成率
12個月就有 108 個欄位
"""
df2 = pd.read_csv('revenue.csv', header=None, index_col=0, na_values=['-'])
df2 = df2.astype(float)
#print(df2.shape)

"""
取得目前股價欄位
"""
df3 = pd.read_csv('company.csv', header=None, index_col=0)
df3 = df3.drop(1, axis=1)
df3 = df3.astype(float)

"""
final_df 總共有 (dogFieldNum * curSeasonNum) + 108 + 1 個欄位
"""
final_df = pd.concat([df1,df2,df3], axis=1, join_axes=[df1.index], ignore_index = True)
#print(org_df.shape)
#print(org_df.columns.tolist())

offset1 = -1 - curSeasonNum # 減去 1 是 column index 從 0 開始, 減去 curSeasonNum 是讓 width1 的乘數可以直接使用欄位號碼
width1 = curSeasonNum
offset2 = 138 - 1 - 9 # 營收欄位共138個 減去 1 是column index從 0 開始, 減去 9 是讓 width2 的乘數可以直接使用月份
width2 = 9 # 營收欄位寬度為9

"""
新增股價淨值比欄位
"""
final_df[combinedFieldNum] = final_df[combinedFieldNum - 1] / final_df[3 * width1 + curSeasonNum + offset1]

"""
新增外部股東報酬率欄位
"""
final_df[combinedFieldNum + 1] = final_df[7 * width1 + curSeasonNum + offset1] / final_df[combinedFieldNum]

# ============================================================

# 挑最新一季ROE>1% 且 上季ROE>1% 且 最新月份營收年增率>20% 且 上個月營收年增率>20% 的股票
selectedList = final_df[(final_df[6 * width1 + curSeasonNum + offset1] > 1) & (final_df[6 * width1 + curSeasonNum - 1 + offset1] > 1) & \
	(final_df[6 + width2 * curMonthNum + offset2] > 20) & (final_df[6 + width2 * (curMonthNum - 1) + offset2] > 20)].index.tolist()

# ============================================================

# 挑最新的近四季ROE大於20% 且 外部股東報酬率大於8%的股票
selectedList = final_df[(final_df[7 * width1 + curSeasonNum + offset1] > 20) & (final_df[combinedFieldNum + 1] > 8)].index.tolist()

# ============================================================

"""
本季營收年增率>=25%
近二季營收年增率是遞增的
本季EPS年增率>=25%
近二季EPS年增率是遞增的
本季ROE>=5%
近四季ROE>=20%
"""
"""
selectedList = final_df[(final_df[9 * width1 + curSeasonNum + offset1] > 25) & \
	(final_df[9 * width1 + curSeasonNum + offset1] > final_df[9 * width1 + (curSeasonNum - 1) + offset1]) & \
	(final_df[21 * width1 + curSeasonNum + offset1] > 25) & \
	(final_df[21 * width1 + curSeasonNum + offset1] > final_df[21 * width1 + (curSeasonNum - 1) + offset1]) & \
	(final_df[6 * width1 + curSeasonNum + offset1] > 5) & (final_df[7 * width1 + curSeasonNum + offset1] > 20)].index.tolist()
"""

# 最新的近四季ROE大於20
selectedList = final_df[(final_df[7 * width1 + curSeasonNum + offset1] > 20)].index.tolist()

outList = []
for item in selectedList:
	try:
		companyName = companyMap[str(item)].name
		fullName = '{}({})'.format(item,companyName)
		outList.append(fullName)
		print(fullName, end=' ')
	except KeyError as e:
		print(e)

writeToFile = True
count = 0
if(writeToFile):
	with open('selected.txt', 'w', encoding='utf-8') as f:
		for item in outList:
			f.write("%s," % item)
			count = count + 1 
			if(count % 10 == 0):
				f.write("\n")
				
