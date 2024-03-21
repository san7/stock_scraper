from urllib.error import HTTPError
from bs4 import BeautifulSoup
from time import sleep

import csv
import json

from common_utils import *

urlReq = getUrlRequest(useProxy=True)


#companyIdList = getCompanyIdList()
companyIdList = ['1101']
#lastIndex = getLastCompanyIdIndex('revenue.csv', companyIdList)
lastIndex = 0

input("Press Enter to continue...")

with open('revenue.csv', 'a', newline='', encoding='utf-8') as fp:
	writer = csv.writer(fp)
	if(lastIndex != 0):
		lastIndex = lastIndex + 1
	for i in range(lastIndex, len(companyIdList)):
		print("scrape company " + companyIdList[i] + "...")
		revenueList = []
		try:
			html = urlReq.urlopen('https://tw.stock.yahoo.com/quote/{}.TW/revenue'.format(companyIdList[i]))
		except HTTPError as e:
			print(e)
		html_content = html.read()
		soup = BeautifulSoup(html_content, "html.parser")
		script_tags = soup.find_all("script")
		for script_tag in script_tags:
			script_content = script_tag.string
			revenue_table_data = None
			if script_content:
				start_index = script_content.find('"revenueTable":')
				if start_index != -1:
					start_index += len('"revenueTable":')
					end_index = script_content.find(',"isFailed"', start_index)
					revenue_table_json = script_content[start_index:end_index] + "}"
					print(revenue_table_json)
					revenue_table_data = json.loads(revenue_table_json)
			if revenue_table_data:
				print("Revenue Table Data:")
				#print(revenue_table_data)
				print(revenue_table_data['data'][0]['date'])
				print(revenue_table_data['data'][1]['date'])
				print(revenue_table_data['data'][2]['date'])
		sleep(1)