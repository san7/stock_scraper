import pandas as pd

from common_utils import *

companyMap = getCompanyMap()

df = pd.read_csv('shareholder.csv', header=None, index_col=0)
df2 = df.astype(float)
#print(df2)

pd.set_option('display.max_columns',200)

selectedList = df2[(df2[1] > df2[2]) & (df2[2] > df2[3]) & (df2[3] > df2[4])].index.tolist()

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
