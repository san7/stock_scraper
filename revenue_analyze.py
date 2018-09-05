import pandas as pd

df = pd.read_csv('revenue.csv', header=None, index_col=0)
df2 = df.astype(float)
#print(df2)
#print(df2.dtypes.value_counts())
#print(df2.index)
#print(df2.columns)

# 前年度月 | 前年度營收 | 前年度年增率 | 今年度月 | 今年度營收 | 今年度年增率 | 今年度累計營收 | 今年度累積營收年增率 | 達成率
# 一共9個欄位 12個月就有108個欄位
pd.set_option('display.max_columns',200)

# 看台積電資料
print(df2.loc[[2330]])

# 看台積電今年度累積營收年增率
for i in range(8,108,9):
	print(df2.loc[2330,i])

# 看每檔的七月累積營收年增率 
print(df2.loc[:,8+9*6])

# 挑七月累積營收年增率 > 20%的股票
print(df2[df2[8+9*6] > 20].index)

# 挑六月累積營收年增率 > 20%的股票 且 挑七月累積營收年增率 > 25%的股票
selectedList = df2[(df2[8+9*5] > 20) & (df2[8+9*6] > 25)].index.tolist()
print(selectedList)

with open('selected.txt', 'w') as f:
	for item in selectedList:
		f.write("%s\n" % item)

