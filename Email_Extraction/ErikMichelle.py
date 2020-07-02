import pandas as pd
import email
from bs4 import BeautifulSoup as bs
from html2text import html2text as h2t
import base64
import re
import nltk
from nltk import wordpunct_tokenize
from nltk.corpus import stopwords
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()
from pprint import pprint
import json
import datetime as dt
from datetime import timedelta as td
import os
import collections
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup as bs
from tqdm._tqdm_notebook import tqdm_notebook as tqdm
import dask.dataframe as dd
from dateutil.tz import tzutc

#from nltk.internals import find_jars_within_path
#st = StanfordNERTagger('stanford-ner-2018-10-16/classifiers/english.all.3class.distsim.crf.ser.gz','stanford-ner-2018-10-16/stanford-ner.jar',encoding='utf-8')

#jar = 'stanford-ner-2018-10-16/stanford-ner.jar'
#model = 'stanford-ner-2018-10-16/classifiers/english.all.3class.distsim.crf.ser.gz'
#ner_tagger = StanfordNERTagger(model, jar, encoding='utf8')


def decodeBase64(encodedStr):
    #print(encodedStr)
    if(encodedStr[:10] == '=?UTF-8?B?' and encodedStr[-2:] == '?='): #only base64 encoded string
        encodedStr = encodedStr[10:-2] #remove start and last 2
        decodedBytes = base64.b64decode(encodedStr)
        decodedStr = str(decodedBytes, "utf-8")
        return decodedStr
    else: #also some text after the encoded string
        return encodedStr
        
        
def splitAndDecode (fullStr):#recognise parts of fullStr as base64 stuff that needs to be decoded
    #print("Let's split this mess! This it what it looks like now:\n" + fullStr)#  
    splits = fullStr.split()
    returnStr = ''
    for split in splits:
        returnStr += decodeBase64(split) + ' '
    returnStr = returnStr[:-1]
    #print("Pfew, done. This is the new string:\n" + returnStr)
    return returnStr

def getbody(msg):
    body = None
    #Walk through the parts of the email to find the text body.    
    if msg.is_multipart():    
        for part in msg.walk():

            # If part is multipart, walk through the subparts.            
            if part.is_multipart(): 

                for subpart in part.walk():
                    if subpart.get_content_type() == 'text/plain':
                        # Get the subpart payload (i.e the message body)
                        body = subpart.get_payload(decode=True) 
                        #charset = subpart.get_charset()

            # Part isn't multipart so get the email body
            elif part.get_content_type() == 'text/plain':
                body = part.get_payload(decode=True)
                #charset = part.get_charset()

    # If this isn't a multi-part message then get the payload (i.e the message body)
    elif msg.get_content_type() == 'text/plain':
        body = msg.get_payload(decode=True) 

   # No checking done to match the charset with the correct part. 
    for charset in getcharsets(msg):
        try:
            body = body.decode(charset)
        except UnicodeDecodeError:
            handleerror("UnicodeDecodeError: encountered.",msg,charset)
        except AttributeError:
             handleerror("AttributeError: encountered" ,msg,charset)
    return body    

def getcharsets(msg):
    charsets = set({})
    for c in msg.get_charsets():
        if c is not None:
            charsets.update([c])
    return charsets

def handleerror(errmsg, emailmsg,cs):
    print()
    print(errmsg)
    print("This error occurred while decoding with ",cs," charset.")
    print("These charsets were found in the one email.",getcharsets(emailmsg))
    print("This is the subject:",emailmsg['subject'])
    print("This is the sender:",emailmsg['From'])
    
def return_payload(row):
    if row['email_raw_object'].is_multipart():
        partlist = []
        for part in row['email_raw_object'].get_payload():
            partlist.append(part.get_payload())
        return partlist
    else:
        return [row['email_raw_object'].get_payload()]

def html_to_text(row):
    part = html_iterator(row['body_raw'])
    return part
    
def html_iterator(html):
    for i, elem in enumerate(html):
        #print(str(i)+': '+str(type(elem)))
        if isinstance(elem, str):
            try:
                html[i] = h2t(html[i])
            except:
                html[i] = html[i]
        elif isinstance(elem, list):
            html[i] = html_iterator(elem)
        elif isinstance(elem, email.message.Message):
            msg = elem.as_string()
            html[i] = html_iterator([msg])
        else: print('-----ERROR-----: '+str(type(elem)))
    return html
        
def text_to_words(row):
    content = row['body_text']
    new_list = list(text_iterator(content))
    word_list=[]
    for part in new_list:
        words = re.split("\W+|_", part)
        lower_words = [word.lower() for word in words]
        word_list.append(lower_words)
    flat_list = list(text_iterator(word_list))
    return flat_list

def text_iterator(text):
    for elem in text:
        if isinstance(elem, collections.abc.Iterable) and not isinstance(elem, (str,bytes)):
            yield from text_iterator(elem)
        else:
            yield elem
            

def detect_language(row):
    '''words = []
    for x in row['body_words']: 
        for y in x: 
            words.append(y)'''
    words = row['body_words']
    languages_ratios = {}
    for language in stopwords.fileids():
        stopwords_set = set(stopwords.words(language))
        words_set = set(words)
        common_elements = words_set.intersection(stopwords_set)
        languages_ratios[language] = len(common_elements)
    most_rated_lang = max(languages_ratios, key=languages_ratios.get)
    return most_rated_lang    


def mail_list(row):
    lst = []
    full_lst = []
    mail_regex = '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}' #regex to recognise email address
    title_regex = '[A-Za-z-]+:' #regex to recognise header such as 'From:'
    mail_reg_2 = "\n[A-Za-z-]+:\n <"+mail_regex #regex to recognise pairs where header and mail address are seperated by a newline
    sender = re.findall(mail_regex, row['sender_email']) #list of mail address in sender_email column (most likely 1 address)
    exclude = ['apwg', 'phishing', 'ecrimex'] #list of words mostly included in the mail addresses to which the phishing mails are sent to report
    exclude = exclude + sender
    mail_filter = lambda s: not any(x in s for x in exclude) #filter that removes mail addresses containing the to be excluded mail addresses
    html_regex = '<[A-Za-z-]+>[A-Za-z-]+:[\s]?<\/[A-Za-z-]+>[^<]*<[^>]*>[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}<\/[A-Za-z-]+>'
    mailto_regex = 'mailto:[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}'
    title_filter = lambda s: not any(x==s for x in ['http:', 'mailto:'])
    for column in [row['email_raw_headers'],row['email_raw_body']]: #check for mail addresses in both the header and the body
        diff_lines = re.findall(mail_reg_2, column)
        correct_addresses = filter(mail_filter, diff_lines) #filter out the excluded mail addresses
        for mail in correct_addresses:
            _, head, m = mail.split('\n')
            full_lst.append((head, m.lower()[2:]))
        for line in column.split('\n'): #check for each line in the mail
            if line.startswith("<html>"): #for pieces of html code, the extraction of mail addresses needs to be done differently
                html_parts = re.findall(html_regex, line)
                for html in html_parts:
                    mailto = re.findall(mailto_regex, html)
                    for m in mailto:
                        html = html.replace(m, '')
                    head = re.findall(title_regex, html)
                    mail = re.findall(mail_regex, html)
                    mail_l = [x.lower() for x in mail]
                    tuples = []
                    if len(mail_l)==0:
                        pass
                    elif len(head)==len(mail_l):
                        for i in range(len(head)):
                            tuples.append((head[i],mail_l[i]))
                        for tup in tuples:
                            for x in exclude:
                                if x in tup[1]:
                                    tuples.remove(tup)
                                    break
                    else:
                        correct_addresses = filter(mail_filter, mail_l) #filter out the excluded mail addresses
                        mail = []
                        for address in correct_addresses:
                            mail.append(address)
                        if len(mail)!=0:
                            if len(head)==0:
                                tuples.append(("Unknown:", mail))
                            elif len(head)==1:
                                tuples.append((head[0], mail))
                            else:
                                title = 'Unknown:'+', '.join(head)
                                for m in mail:
                                    tuples.append((title, m))
                    if len(tuples)>0:
                        for tup in tuples:
                            full_lst.append(tup)
            else:
                addresses = re.findall(mail_regex, line) #in plain text, search for mail addresses on each line
                addresses_l = [x.lower() for x in addresses] #make all characters lowercase for comparison with exclusion list
                correct_addresses = filter(mail_filter, addresses_l) #filter out the excluded mail addresses
                mail = []
                for address in correct_addresses: #for each correct address:
                    #lst.append(address) #save the address to a list
                    line = line.replace(address, '') #and remove it from the text line
                    mail.append(address)
                title_line_lst = re.findall(title_regex, line) #look for header in the line with the address
                real_titles = filter(title_filter, title_line_lst) #remove http: & mailto: from list
                head = []
                for title in real_titles:
                    head.append(title)
                if len(mail)==0: pass
                elif len(mail)==len(head):
                    for i in range(len(head)):
                        full_lst.append((head[i],mail[i]))
                elif len(head)==0:
                    for address in mail:
                        full_lst.append(("Unknown:", address))
                else: 
                    title = 'Unknown:'+', '.join(head)
                    for m in mail:
                        full_lst.append((title, m))
    full_set = set(full_lst)
    remove_set = set([])
    if len(full_set)>1:
        for s in full_set:
            if s[0]=="Unknown:":
                b = False
                new_set = full_set.copy()
                new_set.remove(s)
                for f in new_set:
                    if f[1]==s[1]:
                        #print(s)
                        #print(full_set)
                        remove_set.add(s)
                        break
    for r in remove_set:
        if r in full_set:
            full_set.remove(r)
    mail_list = []
    for f in full_set:
        mail_list.append(f)
    return mail_list

def remove_nest(lst, new_lst):
    for l in lst:
        if type(l) == list:
            remove_nest(l, new_lst)
        else:
            new_lst.append(l)
    return new_lst

def ner_tagger(row):
    entities = []
    flat = []
    flat_list = remove_nest(row['body_raw'], flat)
    html = ' '.join(flat_list)

    style_regex = '<style[^>]*>[^<]*</style>'
    tag_regex = '<[^>]*>'

    style = re.findall(style_regex, html)
    for s in style:
        html = html.replace(s, '')

    tags = re.findall(tag_regex, html)
    for t in tags:
        html = html.replace(t, '')

    soup = bs(html)
    text = soup.get_text()
    tokenized_text = word_tokenize(text)
    classified_text = st.tag(tokenized_text)

    for tup in classified_text:
        if tup[1]!='O':
            entities.append(tup)
    
    return entities

def create_columns(phishdf):
    print('change date-type')
    phishdfs = phishdf.copy() #phisdf structured

    print('create and extract mail object')
    phishdfs['email_raw_total'] = phishdfs['email_raw_headers']+phishdfs['email_raw_body']
    phishdfs['email_raw_object'] = phishdfs.email_raw_total.apply(lambda x: email.message_from_string(x))
    
    phishdfs['from'] = phishdfs.email_raw_object.apply(lambda x: x['from'])
    phishdfs['to'] = phishdfs.email_raw_object.apply(lambda x: x['to'])
    phishdfs['subject'] = phishdfs.email_raw_object.apply(lambda x: x['subject'])
    phishdfs['date'] = phishdfs.email_raw_object.apply(lambda x: x['date'])
    phishdfs['content-type'] = phishdfs.email_raw_object.apply(lambda x: x['content-type'])
    phishdfs['return-path'] = phishdfs.email_raw_object.apply(lambda x: x['return-path'])
    
    phishdfs['local_time'] = phishdfs.date.apply(lambda x: x.split()[-2])

    print('payload')
    phishdfs['body_raw'] = phishdfs.apply(return_payload, axis=1)
    print('html to text')
    phishdfs['body_text'] = phishdfs.apply(html_to_text, axis=1)
    print('text to word list')
    phishdfs['body_words'] = phishdfs.apply(text_to_words, axis=1)
    print('detect language')
    phishdfs['language'] = phishdfs.apply(detect_language, axis=1)
    '''
    #Replace are base64 encoded splits in str fields with the decoded version.
    for col in list(phishdfs):
        if(isinstance(phishdfs.loc[1,col], str)):
            for i in phishdfs.index:
                phishdfs.loc[i,col] = splitAndDecode(phishdfs.loc[i,col])
    '''
    #tqdm.pandas(desc='detect email addresses')
    phishdfs['addresses'] = phishdfs.apply(mail_list, axis=1)#, meta=('addresses', object))
    #tqdm.pandas(desc='detect names')
    #phishdfs['names'] = phishdfs.progress_apply(ner_tagger, axis=1)#, meta=('names', object)) #er zijn nu wat html to text dingen overbodig

    return phishdfs

def split_df(phishdfs):
    #checking the errored emails
    errphishdfs = phishdfs[phishdfs['body_text']=='0']
    errphishdfsc = errphishdfs.drop(columns=['body_raw', 'body_text', 'body_words', 'language'])
    
    goodphishdfs = phishdfs[phishdfs['body_text']!='0']
    accepted_languages = ['english', 'dutch', 'german', 'french']
    goodphishdfsl = goodphishdfs[goodphishdfs['language'].isin(accepted_languages)]
#     small_phishdfs = goodphishdfsl#.drop(['email_raw_total', 'email_raw_body', 'email_raw_headers', 'body_words'], axis=1)#[['id', 'date_sent', 'date_received', 'date','from', 'to', 'return-path', 'content-type', 'subject', 'email_raw_total', 'body_raw', 'body_text', 'body_words', 'language', 'addresses']].copy()
    #small_phishdfs['names'] = small_phishdfs.apply(detect_names, axis=1)
    
    wrong_lang = goodphishdfs[~goodphishdfs['language'].isin(accepted_languages)]
    
    return errphishdfsc, goodphishdfsl, wrong_lang

