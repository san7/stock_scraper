import pandas as pd

from common_utils import *

companyMap = getCompanyMap()

offset1 = 1 # 大股東持有率(>1000張),過去七週
offset2 = 8 # 平均張數/股東,過去七週

df = pd.read_csv('shareholder.csv', header=None, index_col=0)
df2 = df.astype(float)
#print(df2)

pd.set_option('display.max_columns',200)

#selectedList = df2[(df2[offset1] < df2[offset1 + 1]) & (df2[offset1 + 1] < df2[offset1 + 2]) & (df2[offset1 + 2] < df2[offset1 + 3])].index.tolist()
#selectedList = df2[(df2[offset1] > df2[offset1 + 1]) & (df2[offset1 + 1] > df2[offset1 + 2]) & (df2[offset1 + 2] > df2[offset1 + 3])].index.tolist()

#selectedList = df2[(df2[offset2] < df2[offset2 + 1]) & (df2[offset2 + 1] < df2[offset2 + 2]) & (df2[offset2 + 2] < df2[offset2 + 3])].index.tolist()
#selectedList = df2[(df2[offset2] > df2[offset2 + 1]) & (df2[offset2 + 1] > df2[offset2 + 2]) & (df2[offset2 + 2] > df2[offset2 + 3])].index.tolist()

#selectedList = df2[(df2[offset1] > df2[offset1 + 1]) & (df2[offset1 + 1] > df2[offset1 + 2]) & \
#    (df2[offset2] > df2[offset2 + 1]) & (df2[offset2 + 1] > df2[offset2 + 2])].index.tolist()
#selectedList = df2[(df2[offset1] < df2[offset1 + 1]) & (df2[offset1 + 1] < df2[offset1 + 2]) & \
#    (df2[offset2] < df2[offset2 + 1]) & (df2[offset2 + 1] < df2[offset2 + 2])].index.tolist()

selectedList = df2[(df2[offset1] - df2[offset1 + 1]) > 1].index.tolist()

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
