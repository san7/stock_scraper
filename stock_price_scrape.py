import os
import datetime
from datetime import date
import pandas as pd
from dateutil import rrule
import json
import time

from common_utils import *

defaultBeginDate = date(2019,8,1)
defaultEndDate = date.today()

urlReq = getUrlRequest(useProxy=True)

companyIdList = getCompanyIdList()

def craw_one_month(stock_number,date):    
    url = "http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=" + date.strftime('%Y%m%d') + "&stockNo=" + str(stock_number)
    print(url)
    jsonData = json.loads(urlReq.urlopen(url).read())
    return pd.DataFrame(jsonData['data'],columns=jsonData['fields'])


if not os.path.exists('./price'):
    os.makedirs('price')
    
for cid in companyIdList:
    hasData = False
    beginDate = defaultBeginDate
    
    try:
        fileName = "./price/{}.csv".format(cid)
        df = pd.read_csv(fileName, index_col=0)
        hasData = True
    except FileNotFoundError:
        pass
    
    if hasData:
        lastRowDate = df.iloc[-1]['日期']
        tmp = [int(x) for x in lastRowDate.split('/')]
        tmp[0] = tmp[0] + 1911
        beginDate = date(*tmp)
        beginDate = beginDate.replace(day=1)
        tmpStr = [x for x in lastRowDate.split('/')]
        df = df[~df['日期'].str.contains(tmpStr[0] + '/' + tmpStr[1])]
    
    if beginDate >= defaultEndDate:
        continue
        
    if hasData:
        result = df
    else:
        result = pd.DataFrame()
    
    for dt in rrule.rrule(rrule.MONTHLY, dtstart=beginDate, until=defaultEndDate):
        result = pd.concat([result,craw_one_month(cid,dt)], ignore_index=True, sort=False)
    
    result.to_csv(('./price/{}.csv').format(cid))
    
    time.sleep(2);
