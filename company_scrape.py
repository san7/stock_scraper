from bs4 import BeautifulSoup

import csv

from common_utils import *


urlReq = getUrlRequest(useProxy=True)


html = urlReq.urlopen('https://stock.wespai.com/p/16647')
bs = BeautifulSoup(html.read(), 'html.parser')
dataList = bs.findAll('td')

with open('company.csv', 'w', newline='', encoding='utf-8') as fp:
	writer = csv.writer(fp)
	if(len(dataList) % 3 != 0):
		print('dataList may be incorrect')
		exit()
	slot = len(dataList) // 3
	for i in range(slot):
		lineDataList = []
		lineDataList.append(dataList[i * 3].get_text())
		lineDataList.append(dataList[i * 3 + 1].get_text())
		lineDataList.append(dataList[i * 3 + 2].get_text())
		writer.writerow(lineDataList)

companyMap = getCompanyMap()
print(companyMap['1102'].name)
print(companyMap['1102'].price)

