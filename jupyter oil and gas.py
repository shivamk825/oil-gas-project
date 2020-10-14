#!/usr/bin/env python
# coding: utf-8

# In[1]:


import datetime
import numpy as np
import requests
from bs4 import BeautifulSoup
import bs4
import re
import http.cookiejar
import urllib.request
import requests
from datetime import date
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import yahoo_fin.stock_info as si
df=pd.read_csv(r'C:/Users/91855/Desktop/oil and gas/oil.csv')

df


# In[ ]:


count=-1
for company in df['compsymbol']:
    count=count+1
    Market_Cap=[]
    Enterprise_Value=[]
    EBITDA_LIST_VALUES=[]
    data_stats_valuation=si.get_stats_valuation(company)
    market_cap=data_stats_valuation.iloc[0]
    market_cap_final=market_cap[1]
    Market_Cap.append(market_cap_final)
    print('-----',company)
    print('marktcp',Market_Cap)
    enterprice_value=data_stats_valuation.iloc[1]
    enterprice_value_final=enterprice_value[1]
    Enterprise_Value.append(enterprice_value_final)
    print('enterpval',Enterprise_Value)
    mydata_stats=si.get_stats(company)
    row_touse=mydata_stats.loc[mydata_stats['Attribute'] == 'EBITDA']
    ebitda_row=row_touse.iloc[0]
    final_ebitda=ebitda_row[1]
    EBITDA_LIST_VALUES.append(final_ebitda)
    print('eb',EBITDA_LIST_VALUES)
    print('----------------API END')
    print('----------------WEBSCRAPING')
    try:
        empl=[]
        time.sleep(3)
        full_profile = 'https://finance.yahoo.com/quote/'+company+'/profile?p=' + company
        print(full_profile)
        r = requests.get(full_profile)
        htmlcontent = r.content
        soup_profile=BeautifulSoup(htmlcontent,'html.parser')
        employee=soup_profile.find_all('p',class_='D(ib) Va(t)')
        for q in employee:
            for e in q.find_all('span',class_='Fw(600)'):
    #             print(e.text)
                empl.append(e.text)
            final_empl=empl[2]
            print('employees',final_empl)
    except ConnectionError:
        print('nooooo')
    if company==company:
        try:
            df['Marketcap'][count]=Market_Cap[0]
        except IndexError:
            print('yes')
        try:                    
            df['Enterprisevalue'][count]=Enterprise_Value[0]
        except IndexError:
            print('yes')
        try:   
            df['Ebitda'][count]=EBITDA_LIST_VALUES[0]
        except IndexError:
            print('yes')
        try:
            df['Employees'][count]=empl[2]
        except IndexError:
            print('yes')
print(Market_Cap)
print(Enterprise_Value)
print(EBITDA_LIST_VALUES)
print(empl)


# In[ ]:


df


# In[ ]:


df.drop("Unnamed: 0",axis=1,inplace=True)
df["Employees"]=df["Employees"].replace({',': ''},regex=True)
df["Ebitda"]=df["Ebitda"].fillna(0)
df['Ebitda']=df['Ebitda'].replace({'K': '*1e3', 'M': '*1e6','B':'*1e9'}, regex=True).map(pd.eval)
df['Enterprisevalue']=df['Enterprisevalue'].replace({'K': '*1e3', 'M': '*1e6','B':'*1e9'}, regex=True).map(pd.eval)
df['Marketcap']=df['Marketcap'].replace({'K': '*1e3', 'M': '*1e6','B':'*1e9'}, regex=True).map(pd.eval)


# In[10]:


df


# In[ ]:


df.to_csv(r'C:/Users/91855/Desktop/oilgas1.csv')


# In[ ]:


#----------------------- to get the pdf url-----------------

d = webdriver.Chrome('C:/Users/91855/Desktop/New folder (2)/chromedriver.exe')
to_use_url=[]
url_found=[]
def togetutl(toput,id_for,d_get):
    global to_use_url
    global url_found
    get=d.get(d_get)
    print('get',get)
    id_value= d.find_element_by_id(id_for)
    print('id_value',id_value)
    time.sleep(3)
    id_value.send_keys(Keys.BACKSPACE * 10)
    print('*****************')
    id_value.send_keys(toput)
    print('--------------')
    time.sleep(3)
    id_value.send_keys(Keys.ENTER)
    time.sleep(3)
    # print(d.current_url)
    to_use_url=d.current_url
    print('touseurl',to_use_url)

for company in df['compsymbol']:
    dates=[]
    a_tags=[]
    togetutl(company,'company','https://www.sec.gov/edgar/searchedgar/companysearch.html')
    togetutl('99','keywords',to_use_url)
    d.get(to_use_url)
    el = d.find_element_by_id('date-range-select')
    for option in el.find_elements_by_tag_name('option'):
        if option.text == 'Custom':
            time.sleep(2)
            option.click()
            break
    select_time = datetime.datetime.now() - datetime.timedelta(days=365)
#     print(select_time.year)
#     print(select_time.month)
#     print(select_time.day)
    from_date = str(select_time.year) + '-' + str(select_time.month) + '-' + str(select_time.day)
    print('from_date',from_date)
    print('to_use_url',to_use_url)
    togetutl(from_date, 'date-from', to_use_url)
    time.sleep(1)
    cliclking=d.find_element_by_id('search')
    time.sleep(1)
    cliclking.click()
    current_report=d.current_url
    print('after click',current_report)
    all_page=d.page_source
#     print('all_page',all_page)
    
    d.get(current_report)
    soup_profile = BeautifulSoup(all_page)
#     print('soup_profile',soup_profile)
    dates=[]
    a_tags=[]
    today = str(datetime.date.today())

    eth_bal = soup_profile.findAll('a', text='8-K (Current report)  EX-99.1')
    print('eth_bal',eth_bal)
    sorted_date=[]
    for i in eth_bal:
        print('iiiiiiii',i)
        a_tags.append(str(i))
        for q in i.find_next('td'):
            print('qqqqqqqqq',q)
            dates.append(q)
            sorted_date=sorted(dates, key=lambda s:datetime.datetime.strptime(s, "%Y-%m-%d").date() - datetime.date.today())
            print('sorted final date',sorted_date[-1])
    print('unsorted date',dates)
    print('unsorted a tags',a_tags)
    index_no_date=dates.index(sorted_date[-1])
    print('FINAL INDEX',index_no_date)
    print('FINAL A TAG',a_tags[index_no_date])
    html_a=a_tags[index_no_date]
    contents = BeautifulSoup(html_a, 'html.parser')
    preview_file=contents.findAll('a',class_='preview-file')
    for i in preview_file:
        pass
    print(i.text)
    print(i['data-adsh'])
    data_file_name=str(i['data-adsh'])
    print(i['data-file-name'])
    data_adsh=i['data-file-name']
    print('THSESE ARE A CONTENTS')
    code = soup_profile.findAll('td', class_='cik d-none',limit=2)
    for i in code:
        # print('code is',i.text)
        pass
    code_str=''
    code_str=i.text[4:]
    print('final code string',code_str)
    country = soup_profile.findAll('td', class_='biz-location located d-none',limit=1)
    for i in country:
        print(i.text)
    print('final code string', str)
    print('data file name',data_file_name)
    print('data_adsh',data_adsh)
    convert_to_string=("'"+data_file_name+"'")
    converted_str= convert_to_string.replace("-", "")
    print('converted_str data_adsh',converted_str)
    converted_final=converted_str[1:-1]
    documenet_download_url='https://www.sec.gov/Archives/edgar/data/'+str(code_str)+'/'+converted_final+'/'+str(data_adsh)
    print(documenet_download_url)
    url_found.append(documenet_download_url)


# In[ ]:


url_found.append('https://www.sec.gov/Archives/edgar/data/0001486159/000148615920000082/dipcreditagreementexec.htm')
url_found[2]='https://www.sec.gov/Archives/edgar/data/0001724965/000119312520070608/d858952dex991.htm'


# In[ ]:


url_found


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[4]:





# In[5]:





# In[ ]:





# In[7]:





# In[8]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





