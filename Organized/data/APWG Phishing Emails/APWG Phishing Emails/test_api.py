#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 13:49:38 2019

@author: abhishta
"""


from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint
from dateutil import parser
from datetime import timedelta as td
import pandas as pd
import matplotlib.pyplot as plt
from pylab import rcParams
import re
rcParams.update({'figure.autolayout': True})

# Configure API key authorization: Authorization
swagger_client.configuration.api_key['Authorization'] = 'dbb73b3d1d7d79868a65f843db141940cef112af'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# swagger_client.configuration.api_key_prefix['Authorization'] = 'Bearer'
# Configure API key authorization: t
swagger_client.configuration.api_key['t'] = 'dbb73b3d1d7d79868a65f843db141940cef112af'


start_day='08-19-2018'
start_day=parser.parse(start_day)
final_day=start_day+td(days=360)
links=list()
idn=list()
date_sent=list()
date_reported=list()
date_received=list()
email_subject=list()
sender_email=list()
recipient_email=list()
email_raw_body=list()
email_raw_headers=list()
email_has_attachments=list()
modified=list()
today=start_day
end_day=start_day+td(minutes=5)
phish_instance=swagger_client.ReportPhishingApi()
month=start_day.month
date_time=list()
counts=list()
while end_day<=final_day:
    #print(today)
    today_epoch=int(today.timestamp())
    end_day_epoch=int(end_day.timestamp())
    try:
        #phish_response = phish_instance.report_phishing_get(mod_date_start=today_epoch, mod_date_end=end_day_epoch) #absolute_href = True, order_by='date_sent', order='asc',
        phish_response = phish_instance.report_phishing_get(date_reported_start=today_epoch, date_reported_end=end_day_epoch, per_page=200) #absolute_href = True, order_by='date_sent', order='asc',
        #pprint(phish_response)
    except ApiException as e:
        print("Exception when calling AdminApi->email_get: %s\n" % e)
    
    phish_dict=phish_response.to_dict()
    mails=phish_dict['embedded']
    total=phish_dict['total']
    total_found=phish_dict['total_found']
    print('%s \t %d'%(today,total_found))
    date_time.append(today)
    counts.append(total_found)
    if total_found>0:
        mails_e=mails['emails']
        keys=mails_e[0].keys()
        
        for mail in mails_e:
            links.append(mail['links'])
            idn.append(mail['id'])
            date_sent.append(mail['date_sent'])
            date_reported.append(mail['date_reported'])
            date_received.append(mail['date_received'])
            email_subject.append(mail['email_subject'])
            sender_email.append(mail['sender_email'])
            recipient_email.append(mail['recipient_email'])
            email_raw_body.append(mail['email_raw_body'])
            email_raw_headers.append(mail['email_raw_headers'])
            email_has_attachments.append(mail['email_has_attachments'])
            modified.append(mail['modified'])
    
    today=end_day
    end_day=today+td(minutes=5)
    year=today.year
    
    if today.month != month:
        phish_df=pd.DataFrame()
        phish_df['id']=idn
        phish_df['date_sent']=date_sent
        phish_df['date_received']=date_received
        phish_df['date_reported']=date_reported
        phish_df['links']=links
        phish_df['sender_email']=sender_email
        phish_df['recipient_email']=recipient_email
        phish_df['email_subject']=email_subject
        phish_df['email_raw_headers']=email_raw_headers
        phish_df['email_raw_body']=email_raw_body
        phish_df['email_has_attachments']=email_has_attachments
        phish_df['modified']=modified
        phish_df.to_json('phish_month_%d_%d.json'%(month,year))
        
        counts_df=pd.DataFrame()
        counts_df['Time Stamp']=date_time
        counts_df['Total Found']=counts
        counts_df.to_csv('total_counts_%d_%d.csv'%(month,year))
        
        month=today.month
        links=list()
        idn=list()
        date_sent=list()
        date_reported=list()
        date_received=list()
        email_subject=list()
        sender_email=list()
        recipient_email=list()
        email_raw_body=list()
        email_raw_headers=list()
        email_has_attachments=list()
        modified=list()
        counts=list()
        date_time=list()
        
        
        

phish_df=pd.DataFrame()
phish_df['id']=idn
phish_df['date_sent']=date_sent
phish_df['date_received']=date_received
phish_df['date_reported']=date_reported
phish_df['links']=links
phish_df['sender_email']=sender_email
phish_df['recipient_email']=recipient_email
phish_df['email_subject']=email_subject
phish_df['email_raw_headers']=email_raw_headers
phish_df['email_raw_body']=email_raw_body
phish_df['email_has_attachments']=email_has_attachments
phish_df['modified']=modified
phish_df.to_json('phish_month_%d.json'%(month,year))

counts_df=pd.DataFrame()
counts_df['Time Stamp']=date_time
counts_df['Total Found']=total_found
counts_df.to_csv('total_counts_%d_%d.csv'%(month,year))


df_8_18=pd.read_csv("total_counts_8_2018.csv")
df_9_18=pd.read_csv("total_counts_9_2018.csv")
df_10_18=pd.read_csv("total_counts_10_2018.csv")
df_11_18=pd.read_csv("total_counts_11_2018.csv")
df_12_18=pd.read_csv("total_counts_12_2018.csv")
df_1_19=pd.read_csv("total_counts_1_2019.csv")
df_2_19=pd.read_csv("total_counts_2_2019.csv")
df_3_19=pd.read_csv("total_counts_3_2019.csv")

frames=[df_8_18, df_9_18, df_10_18, df_11_18, df_12_18, df_1_19, df_2_19, df_3_19]
total_counts_df=pd.concat(frames)


total_counts_df['Time Stamp']=pd.to_datetime(total_counts_df['Time Stamp'])

#plt.plot(x=total_counts_df['Time Stamp'], y=total_counts_df['Total Found'])
total_counts_df.plot(x='Time Stamp', y='Total Found')
plt.xticks(rotation=70)
plt.show()
plt.close()

#Groupplots

total_counts_df.index=total_counts_df['Time Stamp']
daily_df=total_counts_df.resample('D').sum()

daily_df.plot(y='Total Found')
plt.xticks(rotation=70)
plt.savefig('Total Phishing Emails.pdf',dpi=500)
plt.show()
plt.close()

#for index,row in phish_df.iterrows():
#    if "ddos" in row['email_raw_body']:
#        p=row['email_raw_body']
#        file=open('ddos_email_%d.txt'%(index),'w')
#        file.writelines(p)
#        file.close()
    


#start_date='08-16-2018'
#start_date=parser.parse(start_date)
#dates=list()
#mails=list()
#for i in range(0,365):
#    print(i)
#    today=start_date+td(days=i)
#    today_epoch=int(today.timestamp())
#    phish_response = phish_instance.report_phishing_get(date_received=today_epoch)
#    dates.append(today.date())
#    mails.append(phish_response.total_found)
#
#df=pd.DataFrame()
#df['Mails']=mails
#df.index=dates
##df.plot()
    
    
    