
HTTP_PROXY = 'http://proxy.xxx.com.tw:8080'
HTTPS_PROXY = 'https://proxy.xxx.com.tw:8080'

MY_USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
MY_DOG_USER_NAME = 'xxxx'
MY_DOG_PASSWORD = 'yyyy'

def getCompanyList():
	companyList = []
	with open('company_out.csv', encoding='utf-8') as fp:
		for line in fp:
			splittedData = line.split(',')
			companyList.append(splittedData[0])
	return companyList
	
		
def getLastCompanyIndex(filename, companyList):
	try:
		with open(filename, 'r', encoding='utf-8') as fp:
			lines = fp.readlines()
			lastLine = lines[-1]
			print('lastLine=' + lastLine + '<<<') 
			lastCompany = lastLine[0:4]
			print('lastCompany=' + lastCompany + '<<<') 
	except Exception as e:
		print(e)
		print('reset lastCompany to None')
		lastCompany = None

	try:
		lastIndex = companyList.index(lastCompany)
		print('lastIndex=' + str(lastIndex))
	except Exception as e:
		print(e)
		print('reset lastIndex to 0')
		lastIndex = 0
	
	return lastIndex

def getCompanyMap():
	companyMap = {}
	with open('company_out.csv', encoding='utf-8') as fp:
		for line in fp:
			splittedData = line.split(',')
			companyMap[splittedData[0]] = splittedData[1]
	return companyMap