from collections import namedtuple

HTTP_PROXY = 'http://proxy.cht.com.tw:8080'
HTTPS_PROXY = 'https://proxy.cht.com.tw:8080'

MY_USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
MY_DOG_USER_NAME = 'xxxx'
MY_DOG_PASSWORD = 'yyyy'

Company = namedtuple('Company','name price')

def getCompanyIdList():
	companyIdList = []
	with open('company.csv', encoding='utf-8') as fp:
		for line in fp:
			splittedData = line.split(',')
			companyIdList.append(splittedData[0])
	return companyIdList
	
		
def getLastCompanyIdIndex(filename, companyIdList):
	try:
		with open(filename, 'r', encoding='utf-8') as fp:
			lines = fp.readlines()
			lastLine = lines[-1]
			print('lastLine=' + lastLine + '<<<') 
			lastCompanyId = lastLine[0:4]
			print('lastCompanyId=' + lastCompanyId + '<<<') 
	except Exception as e:
		print(e)
		print('reset lastCompanyId to None')
		lastCompanyId = None

	try:
		lastIndex = companyIdList.index(lastCompanyId)
		print('lastIndex=' + str(lastIndex))
	except Exception as e:
		print(e)
		print('reset lastIndex to 0')
		lastIndex = 0
	
	return lastIndex

def getCompanyMap():
	companyMap = {}
	with open('company.csv', encoding='utf-8') as fp:
		for line in fp:
			splittedData = line.split(',')
			companyMap[splittedData[0]] = Company(splittedData[1],splittedData[2])
	return companyMap

