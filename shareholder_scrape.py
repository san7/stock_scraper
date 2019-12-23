from urllib.error import HTTPError
from bs4 import BeautifulSoup
from time import sleep

import re
import csv

from common_utils import *

urlReq = getUrlRequest(useProxy=True)
companyIdList = getCompanyIdList()
lastIndex = getLastCompanyIdIndex('shareholder.csv', companyIdList)

input("Press Enter to continue...")

with open('shareholder.csv', 'a', newline='', encoding='utf-8') as fp:
	writer = csv.writer(fp)
	if(lastIndex != 0):
		lastIndex = lastIndex + 1
	for i in range(lastIndex, len(companyIdList)):
		print("scrape company " + companyIdList[i] + "...")
		shareholderList = []
		try:
			html = urlReq.urlopen('https://norway.twsthr.info/StockHolders.aspx?stock={}'.format(companyIdList[i]))
		except HTTPError as e:
			print(e)
		content = html.read().decode('utf-8')
		index = content.find("大股東持有率(>1000張)")
		if index == -1:
			continue
		index2 = content.rfind("data:",0,index)
		if index2 == -1:
			continue
		data = content[index2 + 7 : index - 10]
		dataList = data.split(", ")
		shareholderList.append(companyIdList[i])		
		shareholderList.extend(dataList[:-8:-1])
		writer.writerow(shareholderList)
		fp.flush()
		sleep(1)






