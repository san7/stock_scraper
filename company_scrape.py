from urllib import request as urlrequest
from bs4 import BeautifulSoup

import csv

from common_utils import *


proxy_support = urlrequest.ProxyHandler({'http' : HTTP_PROXY, 
                                         'https': HTTPS_PROXY})
opener = urlrequest.build_opener(proxy_support)
opener.addheaders = [('User-agent', MY_USER_AGENT)]
urlrequest.install_opener(opener)

html = urlrequest.urlopen('https://stock.wespai.com/p/16647')
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

