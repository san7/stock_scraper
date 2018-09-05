
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