from bs4 import BeautifulSoup
from time import sleep

import requests
import json
import csv

from common_utils import *


# 可調整的參數
targetDataIdList = ['ROET4Q']
queryRange = '2022/2023'
curSeasonNum = 8

use_proxy = True

if use_proxy:
	proxies = { 'http' : HTTP_PROXY, 'https': HTTPS_PROXY }
else:
	proxies = None

headers = {'User-Agent' : MY_USER_AGENT}

companyIdList = getCompanyIdList()
lastIndex = getLastCompanyIdIndex('dog.csv', companyIdList)

input("Press Enter to continue...")

session = requests.Session()
r1 = session.get('https://statementdog.com/users/sign_in', headers = headers, proxies=proxies)
bs = BeautifulSoup(r1.text, 'html.parser')
token = bs.select('input[name="authenticity_token"]')[0]['value']
#print(token)
userCtx = getUserCtx()
params = {'authenticity_token' : token, 'user[email]': userCtx.name, 'user[password]': userCtx.password, 'user[remember_me]' : '1'}
r2 = session.post('https://statementdog.com/users/sign_in', headers = headers, data = params, proxies=proxies)
print(r2)
#print(r2.cookies.get_dict())

with open('dog.csv', 'a', newline='', encoding='utf-8') as fp:
	writer = csv.writer(fp)
	if(lastIndex != 0):
		lastIndex = lastIndex + 1
	for i in range(lastIndex, len(companyIdList)):
		print("scrape company " + companyIdList[i] + "...")
		compStatsList = []
		isNoErr = True
		url = 'https://statementdog.com/api/v2/fundamentals/{}/{}/cf?qbu=true&qf=analysis'.format(companyIdList[i], queryRange)
		try:
			r3 = session.get(url, headers = headers, proxies=proxies)
			jsonObj = json.loads(r3.text)
			compStatsList.append(companyIdList[i])
			for dataId in targetDataIdList:
				for seasonIdx in range(curSeasonNum):
					print(jsonObj['quarterly'][dataId]['data'][seasonIdx][1])
					compStatsList.append(jsonObj['quarterly'][dataId]['data'][seasonIdx][1])
		except Exception as e:
			print(e)
			isNoErr = False
		if(isNoErr):			
			writer.writerow(compStatsList)
			fp.flush()
		sleep(2)		
		









