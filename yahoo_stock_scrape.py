from urllib import request as urlrequest
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from time import sleep

import re
import csv

from common_utils import *

proxy_support = urlrequest.ProxyHandler({'http' : HTTP_PROXY, 
                                         'https': HTTPS_PROXY})
opener = urlrequest.build_opener(proxy_support)
opener.addheaders = [('User-agent', MY_USER_AGENT)]
urlrequest.install_opener(opener)


companyList = getCompanyList()
#print(companyList)
lastIndex = getLastCompanyIndex('revenue.csv', companyList)

input("Press Enter to continue...")


startIdx = 12 # 前面多餘資料的個數
stepSize = 9 # 一列有9個資料欄位
step = 12 # 一共12列(12個月)
endIdx = startIdx + stepSize * step

with open('revenue.csv', 'a', newline='', encoding='utf-8') as fp:
	writer = csv.writer(fp)
	if(lastIndex != 0):
		lastIndex = lastIndex + 1
	for i in range(lastIndex, len(companyList)):
		print("scrape company " + companyList[i] + "...")
		revenueList = []
		try:
			html = urlrequest.urlopen('https://tw.stock.yahoo.com/d/s/earning_{}.html'.format(companyList[i]))
		except HTTPError as e:
			print(e)
		bs = BeautifulSoup(html.read(), 'html.parser')
		dataList = bs.findAll('td', {'class':'ttt'})
		revenueList.append(companyList[i])		
		for j in range(startIdx, endIdx, stepSize):
			tmpList = [re.sub(',|%|-', '', data.get_text()) for data in dataList[j : j + stepSize]]
			revenueList.extend(tmpList)
		writer.writerow(revenueList)
		fp.flush()
		sleep(1)






