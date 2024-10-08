#!/usr/bin/env python
# coding: utf-8

def web_scrapper(stock):
    headers = {
    'accept-language': 'en-US,en;q=0.9',
    'origin': 'https://www.nasdaq.com/',
    'referer': 'https://www.nasdaq.com/',
    'accept': 'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
}

    data = requests.get('https://api.nasdaq.com/api/company/'+stock+'/financials?frequency=1', headers=headers).json()
    if (data != None):
        if (data["data"] != None):
            if (data["data"]["incomeStatementTable"] != None and data["data"]["balanceSheetTable"] != None and data["data"]["cashFlowTable"] != None):
                    incomesheetstatement = data["data"]["incomeStatementTable"]
                    balancesheetstatement = data["data"]["balanceSheetTable"]
                    cashflowstatement = data["data"]["cashFlowTable"]
            else:
                incomesheetstatement = "NULL"
                balancesheetstatement = "NULL"
                cashflowstatement = "NULL"
        else:
            incomesheetstatement = "NULL"
            balancesheetstatement = "NULL"
            cashflowstatement = "NULL"
    else:
        incomesheetstatement = "NULL"
        balancesheetstatement = "NULL"
        cashflowstatement = "NULL"

    return incomesheetstatement,balancesheetstatement,cashflowstatement


# In[4]:


def dataclean(incomesheetstatement,balancesheetstatement,cashflowstatement):
    inss = bss = cfs = inss_v = bss_v = cfs_v = []
    for i in incomesheetstatement['rows']:
        if i['value2'] == '--' or i['value2'] == '':
            del i
        else:
            j = i['value2'].replace('$','')
            k = j.replace(',','')
            inss.append(i['value1'])
            inss_v.append(float(k))
    for i in balancesheetstatement['rows']:
        if i['value2'] == '--' or i['value2'] == '':
            del i
        else:
            j = i['value2'].replace('$','')
            k = j.replace(',','')
            bss.append(i['value1'])
            bss_v.append(float(k))
    for i in cashflowstatement['rows']:
        if i['value2'] == '--' or i['value2'] == '':
            del i
        else:
            j = i['value2'].replace('$','')
            k = j.replace(',','')
            cfs.append(i['value1'])
            cfs_v.append(float(k))
    return inss,inss_v,bss,bss_v,cfs,cfs_v

def incomestatement(stock,incomesheetstatement,inss,inss_v,bss,bss_v,cfs,cfs_v):
    date = incomesheetstatement['headers']['value2']
    try:
        gpm = (inss_v[inss.index('Gross Profit')]/inss_v[inss.index('Total Revenue')])*100
        print("Gross Profit Margin for {0} is as per {1} is: {2}".format(stock,date,round(gpm,3)))
    except:
        pass
    try:
        opm = (inss_v[inss.index('Operating Income')]/inss_v[inss.index('Total Revenue')])*100
        print("Operating Profit Margin for {0} is as per {1} is: {2}".format(stock,date,round(opm,3)))
    except:
        pass
    try:
        npm = (inss_v[inss.index('Net Income')]/inss_v[inss.index('Total Revenue')])*100
        print("Net Profit Margin for {0} is as per {1} is: {2}".format(stock,date,round(npm,3)))
    except:
        pass
    try:
        ebitm = (inss_v[inss.index('Earnings Before Interest and Tax')]/inss_v[inss.index('Total Revenue')])*100
        print("Earnings Before Interest and Tax Margin for {0} is as per {1} is: {2}".format(stock,date,round(ebitm,3)))
    except:
        pass
    try:
        oer = (inss_v[inss.index('Operating Expenses')]/inss_v[inss.index('Total Revenue')])*100
        print("Operating Expense Ratio for {0} is as per {1} is: {2}".format(stock,date,round(oer,3)))
    except:
        pass
    try:
        icr = (inss_v[inss.index('Operating Income')]/inss_v[inss.index('Interest Expense')])
        print("Interest Coverage Ratio for {0} is as per {1} is: {2}".format(stock,date,round(icr,3)))
    except:
        pass
    try:
        cr = (bss_v[bss.index('Current Assets')]/bss_v[bss.index('Current Liabilities')])
        print("Current Ratio for {0} is as per {1} is: {2}".format(stock,date,round(cr,3)))
    except:
        pass
    try:
        qr = (bss_v[bss.index('Current Assets')]-bss_v[bss.index('Inventory')]/bss_v[bss.index('Current Liabilities')])
        print("Quick Ratio for {0} is as per {1} is: {2}".format(stock,date,round(qr,3)))
    except:
        pass
    try:
        wc = (bss_v[bss.index('Current Assets')]-bss_v[bss.index('Current Liabilities')])
        print("Working Capital for {0} is as per {1} is: {2}".format(stock,date,round(wc,3)))
    except:
        pass
    try:
        der = (bss_v[bss.index('Total Liabilities')]/bss_v[bss.index('Total Equity')])
        print("Debit to equity ratio for {0} is as per {1} is: {2}".format(stock,date,round(der,3)))
    except:
        pass
    try:
        roa = (inss_v[inss.index('Net Income')]/bss_v[bss.index('Total Assets')])*100
        print("Return on Assets for {0} is as per {1} is: {2}".format(stock,date,round(roa,3)))
    except:
        pass
    try:
        roe = (inss_v[inss.index('Net Income')]/bss_v[bss.index('Total Equity')])*100#wrong
        print("Retrun on Equity for {0} is as per {1} is: {2}".format(stock,date,round(roe,3)))
    except:
        pass
    try:
        icr = (inss_v[inss.index('Operating Income')]/inss_v[inss.index('Interest Expense')])*100
        print("Interest Coverage Ratio for {0} is as per {1} is: {2}".format(stock,date,round(icr,3)))
    except:
        pass

import requests

while(True):
    stock = input("Enter the stock ticker (Ex. AAPL): ")
    incomesheetstatement,balancesheetstatement,cashflowstatement = web_scrapper(stock)
    if incomesheetstatement != "NULL" and balancesheetstatement != "NULL" and cashflowstatement != "NULL":
        inss,inss_v,bss,bss_v,cfs,cfs_v = dataclean(incomesheetstatement,balancesheetstatement,cashflowstatement)
        incomestatement(stock,incomesheetstatement,inss,inss_v,bss,bss_v,cfs,cfs_v)
    else:
        print('Try Input the New Stock!')




