from bs4 import BeautifulSoup
from time import sleep

import requests
import json
import csv

"""
"65":{"label":"EPS","data":[[0,"1.53"],[1,"2.0"],[2,"2.0"],[3,"1.73"],[4,"1.85"],[5,"2.3"],[6,"2.94"],[7,"3.09"],[8,"3.05"],[9,"3.06"],[10,"2.91"],
		[11,"2.81"],[12,"2.5"],[13,"2.8"],[14,"3.73"],[15,"3.86"],[16,"3.38"],[17,"2.56"],[18,"3.47"],[19,"3.83"],[20,"3.46"],[21,"2.79"]]},
"66":{"label":"近四季EPS"
"77":{"label":"每股淨值"
"95":{"label":"毛利率"
"96":{"label":"營業利益率"
"99":{"label":"ROE"
"101":{"label":"近四季ROE"
"107":{"label":"單季營收季增率"
"108":{"label":"單季營收年增率"
"109":{"label":"近4季營收季增率"
"110":{"label":"近4季營收年增率"
"111":{"label":"單季毛利季增率"
"112":{"label":"單季毛利年增率"
"113":{"label":"近4季毛利季增率"
"114":{"label":"近4季毛利年增率"
"115":{"label":"單季營業利益季增率"
"116":{"label":"單季營業利益年增率"
"117":{"label":"近4季營業利益季增率"
"118":{"label":"近4季營業利益年增率"
"123":{"label":"單季EPS季增率"
"124":{"label":"單季EPS年增率"
"125":{"label":"近4季EPS季增率"
"126":{"label":"近4季EPS年增率"
"""
targetDataIdList = ['65','66','77','95','96','99','101','107','108','109','110','111','112','113',
	'114','115','116','117','118','123','124','125','126']
seasonNum = 6

proxies = {
  'http': 'http://proxy.cht.com.tw:8080',
  'https': 'https://proxy.cht.com.tw:8080',
}

companyList = []
with open('company_out.csv', encoding='utf-8') as fp:
	for line in fp:
		splittedData = line.split(',')
		companyList.append(splittedData[0])
#print(companyList)


try:
	with open('dog.csv', 'r', encoding='utf-8') as fp:
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

session = requests.Session()
r1 = session.get('https://statementdog.com/users/sign_in', proxies=proxies)
bs = BeautifulSoup(r1.text, 'html.parser')
token = bs.select('input[name="authenticity_token"]')[0]['value']
#print(token)
params = {'authenticity_token' : token, 'user[email]': 'xxxx', 'user[password]': 'yyyy', 'user[remember_me]' : '1'}
r2 = session.post('https://statementdog.com/users/sign_in', data = params, proxies=proxies)
print(r2)
#print(r2.cookies.get_dict())

with open('dog.csv', 'a', newline='', encoding='utf-8') as fp:
	writer = csv.writer(fp)
	if(lastIndex != 0):
		lastIndex = lastIndex + 1
	for i in range(lastIndex, len(companyList)):
		print("scrape company " + companyList[i] + "...")
		compStatsList = []
		url = 'https://statementdog.com/api/v1/fundamentals/{}/2017/1/2018/4/cf?queried_by_user=true&_=15'.format(companyList[i])
		r3 = session.get(url, proxies=proxies)
		jsonObj = json.loads(r3.text)
		compStatsList.append(companyList[i])
		for dataId in targetDataIdList:
			for seasonIdx in range(seasonNum):
				#print(jsonObj[dataId]['data'][seasonIdx][1])
				compStatsList.append(jsonObj[dataId]['data'][seasonIdx][1])
		writer.writerow(compStatsList)
		fp.flush()
		sleep(1)		
		









