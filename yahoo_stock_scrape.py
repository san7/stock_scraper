from urllib import request as urlrequest
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from time import sleep

import re
import csv

proxy_support = urlrequest.ProxyHandler({'http' : 'http://proxy.cht.com.tw:8080', 
                                         'https': 'https://proxy.cht.com.tw:8080'})
opener = urlrequest.build_opener(proxy_support)
urlrequest.install_opener(opener)


companyList = []
with open('company_out.csv', encoding='utf-8') as fp:
	for line in fp:
		splittedData = line.split(',')
		companyList.append(splittedData[0])
#print(companyList)


try:
	with open('revenue.csv', 'r', encoding='utf-8') as fp:
		lines = fp.readlines()
		lastLine = lines[-1]
		lastCompany = lastLine[0:4]
except Exception as e:
	print(e)
	lastCompany = None
print('lastCompany=' + str(lastCompany))

try:
	lastIndex = companyList.index(lastCompany)
except:
	lastIndex = 0
print('lastIndex=' + str(lastIndex))

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
		sleep(0.5)






