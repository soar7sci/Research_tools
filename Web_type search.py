# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.6
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# +
#Elesiver/ACS/Wiley/Science/Nature/RSC

#libraries and primary settings
import requests                                         #for controlling the html webpage
from selenium import webdriver                          #for using the automated webbrowser
from bs4 import BeautifulSoup                           #for controlling the html webpage
import time                                             #for waiting webpage loading time
import csv                                              #for saving csv format
import pandas as pd                                     #for controlling csv as database
from crossref.restful import Works                      #for searching database from crossref
from pybliometrics.scopus import AbstractRetrieval      #for searching database from scopus


browser = webdriver.Firefox(executable_path="./geckodriver.exe")
options=webdriver.FirefoxOptions()
options.add_argument("window-size=1920x1080")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0")
# 'user-agent' option may need to be updated, check from 'https://www.whatismybrowser.com/detect/what-is-my-user-agent'

# +
#Functions

# scopus_doi normally shows more paper_data than crossref_doi

# scopus_doi: Save the data (title, doi, journal, year, author, affiliation, Country) from Scopus based on doi    
def scopus_doi(doi_num):
    results=AbstractRetrieval(doi_num)
    paper_data=[]
    authors=[]
    affils=[]
    countrys=[]
    paper_data.append(results.title)
    paper_data.append('http://dx.doi.org/'+doi_num)
    paper_data.append(results.publicationName)
    paper_data.append(results.coverDate[:4])
    for author in results.authors:
        try:
            authors.append(author.given_name+' '+author.surname)
        except:
            authors.append(author.surname)
    for affil in results.affiliation:
        append_list(affils,affil.name)
        append_list(countrys,affil.country)
    
    
    paper_data.append(authors)
    paper_data.append(affils)
    paper_data.append(countrys)
    writer.writerow(paper_data)  

#crossref_doi: Save the data (title, doi, journal, year, author, affiliation) from crossref based on doi
def crossref_doi(doi_num):
    works = Works()
    results=works.doi(doi_num)
    paper_data=[]
    authors=[]
    affil=[]
    paper_data.append(results['title'][0])
    paper_data.append('http://dx.doi.org/'+doi_num)
    paper_data.append(results['container-title'][0])
    paper_data.append(results['created']['date-parts'][0][0])
    for author in results['author']:
        try:
            authors.append(author['given']+' '+author['family'])
        except:
            authors.append(author['family'])
        if author['affiliation']==[]:
            continue
        else:
            if author['affiliation'][0]['name'] in affil:
                continue
            else:
                affil.append(author['affiliation'][0]['name'])
    paper_data.append(authors)
    paper_data.append(affil)
    writer.writerow(paper_data)

#test_crossref_doi: Print the data (title, doi, journal, year, author, affiliation) from crossref based on doi
def test_crossref_doi(doi_num):
    works = Works()
    results=works.doi(doi_num)
    paper_data=[]
    authors=[]
    affil=[]
    paper_data.append(results['title'][0])
    paper_data.append('http://dx.doi.org/'+doi_num)
    paper_data.append(results['container-title'][0])
    paper_data.append(results['created']['date-parts'][0][0])
    for author in results['author']:
        try:
            authors.append(author['given']+' '+author['family'])
        except:
            authors.append(author['family'])
        if author['affiliation']==[]:
            continue
        else:
            if author['affiliation'][0]['name'] in affil:
                continue
            else:
                affil.append(author['affiliation'][0]['name'])
    paper_data.append(authors)
    paper_data.append(affil)
    print(paper_data)

# test_scopus_doi: Print the data (title, doi, journal, year, author, affiliation, Country) from Scopus based on doi
def test_scopus_doi(doi_num):
    results=AbstractRetrieval(doi_num)
    paper_data=[]
    authors=[]
    affils=[]
    countrys=[]
    paper_data.append(results.title)
    paper_data.append('http://dx.doi.org/'+doi_num)
    paper_data.append(results.publicationName)
    paper_data.append(results.coverDate[:4])
    for author in results.authors:
        try:
            authors.append(author.given_name+' '+author.surname)
        except:
            authors.append(author.surname)
    for affil in results.affiliation:
        append_list(affils,affil.name)
        append_list(countrys,affil.country)
    
    
    paper_data.append(authors)
    paper_data.append(affils)
    paper_data.append(countrys)
    print(paper_data)

# # add_scopus_author_affil_country: return paper_data(authors, affils, countrys) from doi_num
# # Used this function for appending paper_data to crossref based database

# def add_scopus_author_affil_country(doi_num):
#     results=AbstractRetrieval(doi_num)
#     paper_data=[]
#     authors=[]
#     affils=[]
#     countrys=[]
    
#     for author in results.authors:
#         try:
#             authors.append(author.given_name+' '+author.surname)
#         except:
#             authors.append(author.surname)
#         #print(type(author['affiliation'][0]))
#     for affil in results.affiliation:
#         append_list(affils,affil.name)
#         append_list(countrys,affil.country)
    
    
#     paper_data.append(authors)
#     paper_data.append(affils)
#     paper_data.append(countrys)
#     return paper_data

# append_list: Append the target if target is not in the li
def append_list(li,target):
    for i in li:
        if target==i:
            return li
    return li.append(target)

# keyword_convert: return webpage address version keyword
# ex) %22all%20solid%20state%20battery%22

def keyword_convert(input_key):
    output_key='%22'
    for i in range(len(input_key)):
        if input_key[i]==' ':
            output_key+='%20'
        else:
            output_key+=input_key[i]
    return output_key+'%22'

# ispaper: return boolean based on article type

def ispaper(article_type):
    false_list=['review','Review', 'REVIEW','cover','COVER','Cover', 'Progress Report','Feature Article', 'Issue',
                'Essay', 'Contents', 'News','ISSUE','Highlight','Highlights','Perspective','Editorial', 'Overview',
                'Frontier','Discussion'
                'Überblick','Forschungsartikel', 'Zuschrift',
                'Preparative Inorganic Chemistry', 'Physical Inorganic Chemistry','Atomic Spectrometry Update']
    true_list=['paper','Communication','ARTICLE','article', 'Article', 'Paper', 
               'Rapid Research Letter','RAPID COMMUNICATION']
    for check in false_list:
        if check in article_type:
            return False
    for check in true_list:
        if check in article_type:
            #print(article_type)
            return True
    print('H '+article_type+' H')
    return False
    
def load_page(url):
    browser.get(url.format(0))
    time.sleep(3)
    return BeautifulSoup(browser.page_source,"lxml")
    
def paper_count(key):
    #keyword=keyword_convert(key)
    keyword=key
    result_journal=[]
    result_journal.append('Total\t')
    result_cnt=[]
    result_cnt.append(0)

    def find_num(text_in):
        text_out=''
        for i in text_in:
            if i=='r':
                break
            elif not i==',':
                text_out+=i
        return text_out
    
    def del_comma(text_in):
        text_out=''
        for i in text_in:
            if not i==',':
                text_out+=i
        return text_out
    
    #ScienceDirect (Elsevior)
    url='https://www.sciencedirect.com/search?qs='+keyword+'&articleTypes=FLA&show=100&offset={}'
    soup=load_page(url)
    try:
        paper_cnt=soup.find('span', attrs={'class':'search-body-results-text'}).get_text()
        paper_cnt=paper_cnt[:len(paper_cnt)-8]
    except:
        paper_cnt='0'
    #print('Elsevior counts:\t'+del_comma(paper_cnt))
    result_journal.append('Elsevior')
    result_cnt.append(int(del_comma(paper_cnt)))
    result_cnt[0]+=int(del_comma(paper_cnt))
    
    #ACS
    url='https://pubs.acs.org/action/doSearch?AllField='+keyword+'&startPage={}&PubType=journals&pageSize=20'
    soup=load_page(url)
    try:
        paper_cnt=soup.find('span', attrs={'class':'result__count'}).get_text()
    except:
        paper_cnt='0'
    #print('ACS\t counts:\t'+del_comma(paper_cnt))
    result_journal.append('ACS\t')
    result_cnt.append(int(del_comma(paper_cnt)))
    result_cnt[0]+=int(del_comma(paper_cnt))

    #Wiley
    url='https://onlinelibrary.wiley.com/action/doSearch?AllField='+keyword+'&PubType=journal&startPage={}&pageSize=20'
    soup=load_page(url)
    try:
        paper_cnt=soup.find('span', attrs={'class':'result__count'}).get_text()
    except:
        paper_cnt='0'
    #print('Wiley\t counts:\t'+del_comma(paper_cnt))
    result_journal.append('Wiley\t')
    result_cnt.append(int(del_comma(paper_cnt)))
    result_cnt[0]+=int(del_comma(paper_cnt))
    
    #RSC
    url='https://pubs.rsc.org/en/results?searchtext='+keyword+'#pnlArticles'
    soup=load_page(url)
    try:
        paper_cnt=soup.find('div', attrs={'class':'fixpadv--l pos--left pagination-summary'}).get_text()[1:10]
    except:
        paper_cnt='0'
    #print('RSC\t counts:\t'+del_comma(paper_cnt))
    result_journal.append('RSC\t')
    result_cnt.append(int(find_num(paper_cnt)))
    result_cnt[0]+=int(find_num(paper_cnt))
    
    #Nature
    url='https://www.nature.com/search?q='+keyword+'&order=relevance&article_type=research&page={}'
    soup=load_page(url.format(1))
    try:
        paper_cnt=soup.find('span', attrs={'class':'u-hide u-show-at-sm'}).next_sibling.get_text()
        paper_cnt=paper_cnt[:len(paper_cnt)-8]
    except:
        paper_cnt='0'
    #print('Nature\t counts:\t'+del_comma(paper_cnt))
    result_journal.append('Nature\t')
    result_cnt.append(int(del_comma(paper_cnt)))
    result_cnt[0]+=int(del_comma(paper_cnt))
    
    #Science
    url='https://www.science.org/action/doSearch?AllField='+keyword+'&pageSize=20&startPage={}'
    soup=load_page(url.format(0))
    try:
        paper_cnt=soup.find('span', attrs={'class':'search-result__meta__item--count'}).get_text()
    except:
        paper_cnt='0'
    #print('Science\t counts:\t'+del_comma(paper_cnt))
    result_journal.append('Science\t')
    result_cnt.append(int(del_comma(paper_cnt)))
    result_cnt[0]+=int(del_comma(paper_cnt))
    
    for i in range(0,7):
        print(result_journal[i]+' : '+str(result_cnt[i])+'\t({:.2f} %)'.format(result_cnt[i]/result_cnt[0]*100))


# +
# 1. ScienceDirect (Elsevior)

# Change list: keyword

# Change keyword as you want in quatation mark
keyword='all solid state battery'

#Open csv file for data saving
filename=keyword+"_Elsevior.csv"
f=open(filename,"w",encoding="utf-8-sig", newline="")
writer=csv.writer(f)
head=["Title","Link","Journal","Year","Authors","Affiliations"]
writer.writerow(head)

#Find last_page number
url='https://www.sciencedirect.com/search?qs='+keyword_convert(keyword)+'&articleTypes=FLA&show=100&offset={}'
soup=load_page(url)
paper_cnt=soup.find('span', attrs={'class':'search-body-results-text'}).get_text()
paper_cnt=paper_cnt[:len(paper_cnt)-8]
last_page=''
for i in paper_cnt:
    if not i==',':
        last_page+=i
last_page=int(int(last_page)/100)+1

for offset in range (0,last_page):
    print("Page: "+str(offset))
    soup=load_page(url.format(offset*100))
    paper_blocks=soup.find_all('li', attrs={'class':'ResultItem col-xs-24 push-m'})
    for paper in paper_blocks:
        try:
            scopus_doi(paper['data-doi'])
        except:
            try:
                crossref_doi(paper['data-doi'])
            except:
                print(paper.find('a', attrs={'class':'result-list-title-link u-font-serif text-s'})['href'])
            
f.close()

# +
# 2. ACS

# Change list: keyword

# Change keyword as you want in quatation mark
keyword='all solid state battery'

#Open csv file for data saving
filename=keyword+"_ACS.csv"
f=open(filename,"w",encoding="utf-8-sig", newline="")
writer=csv.writer(f)
head=["Title","Link","Journal","Year","Authors","Affiliations"]
writer.writerow(head)

#Find last_page number
url='https://pubs.acs.org/action/doSearch?AllField='+keyword_convert(keyword)+'&startPage={}&PubType=journals&pageSize=20'
soup=load_page(url)
paper_cnt=soup.find('span', attrs={'class':'result__count'}).get_text()
last_page=int(int(paper_cnt)/20)+1

for offset in range (0,last_page):
    print("Page: "+str(offset))
    soup=load_page(url.format(offset))
    paper_blocks=soup.find_all('div', attrs={'class':'issue-item clearfix'})
    for paper in paper_blocks:
        try:
            paper_type=paper.find('div', attrs={'class':'infoType'}).get_text()
            #ACS cannot filter the article type
            cur_doi=paper.find('span',attrs={'class':'issue-item_doi'}).get_text()[5:]
        except:
            continue
        
        if ispaper(paper_type):
            try:
                scopus_doi(cur_doi)
            except:
                try:
                    crossref_doi(cur_doi)
                except:
                    print(paper.find('h2',attrs={'class':'issue-item_title'}).a.get_text())
            

f.close()

#results
#with affiliations
#1st: mostly department, 2nd: mostly main institute, last: nationality

# +
# 3. Wiley

# Change list: keyword

# Change keyword as you want in quatation mark
keyword='all solid state battery'

#Open csv file for data saving
filename=keyword+"_Wiley.csv"
f=open(filename,"w",encoding="utf-8-sig", newline="")
writer=csv.writer(f)
head=["Title","Link","Journal","Year","Authors","Affiliations"]
writer.writerow(head)


#Find last_page number
url='https://onlinelibrary.wiley.com/action/doSearch?AllField='+keyword_convert(keyword)+'&PubType=journal&startPage={}&pageSize=20'
soup=load_page(url)
paper_cnt=soup.find('span', attrs={'class':'result__count'}).get_text()
last_page=int(int(paper_cnt)/20)+1

#Scrapping the papers from searched webpage
for offset in range (0,last_page):
    print("Page: "+str(offset))
    #url='https://onlinelibrary.wiley.com/action/doSearch?AllField=%22in-situ+TEM%22&PubType=journal&startPage={}&pageSize=20'.format(offset)
    soup=load_page(url.format(offset))
    count=0
    paper_blocks=soup.find_all('li', attrs={'class':'clearfix separator search__item bulkDownloadWrapper'})
    for paper in paper_blocks:
        count+=1
        try:
            paper_type=paper.find('span', attrs={'class':'meta__type'}).get_text()
            cur_doi=paper.find('a',attrs={'class':'publication_title visitable'})['href'][5:]
        except:
            continue
        
        if ispaper(paper_type):
            try:
                #print(paper.find('a',attrs={'class':'publication_title visitable'})['href'][5:])
                scopus_doi(cur_doi)
            except:
                try:
                    crossref_doi(cur_doi)
                except:
                    print(paper.find('h2',attrs={'class':'issue-item_title'}).a.get_text())
                    #print('error position: '+'Page('+str(offset)+')+count('+str(count)+')')


f.close()

#results
#some has affilliation

# +
# 4. Science

# Change list: keyword

# Change keyword as you want in quatation mark
keyword='all solid state battery'

#Open csv file for data saving
filename=keyword+"_Science.csv"
f=open(filename,"w",encoding="utf-8-sig", newline="")
writer=csv.writer(f)
head=["Title","Link","Journal","Year","Authors","Affiliations"]
writer.writerow(head)

#Find last_page number
url='https://www.science.org/action/doSearch?AllField='+keyword_convert(keyword)+'&pageSize=20&startPage={}'
soup=load_page(url.format(0))
paper_cnt=soup.find('span', attrs={'class':'search-result__meta__item--count'}).get_text()
last_page=int(int(paper_cnt)/20)+1

#Scrapping the papers from searched webpage
for offset in range (0,last_page):
    print("Page: "+str(offset))
    browser.get(url.format(offset))
    time.sleep(3)
    soup=BeautifulSoup(browser.page_source,"lxml")
    paper_blocks=soup.find_all('div', attrs={'class':'card pb-3 mb-4 border-bottom'})
    for paper in paper_blocks:
        cur_doi=paper.find('a',attrs={'class':'text-reset animation-underline'})['href'][5:]
        try:
            scopus_doi(cur_doi)
        except:
            try:
                crossref_doi(cur_doi)
            except:
                print(paper.find('h2',attrs={'class':'issue-item_title'}).a.get_text())

f.close()

# +
# 5. Nature

# Change list: keyword

# Change keyword as you want in quatation mark
keyword='all solid state battery'

#Open csv file for data saving
filename=keyword+"_Nature.csv"
f=open(filename,"w",encoding="utf-8-sig", newline="")
writer=csv.writer(f)
head=["Title","Link","Journal","Year","Authors","Affiliations"]
writer.writerow(head)

#Find last_page number
url='https://www.nature.com/search?q='+keyword_convert(keyword)+'&order=relevance&article_type=research&page={}'
soup=load_page(url.format(1))
paper_cnt=soup.find('span', attrs={'class':'u-hide u-show-at-sm'}).next_sibling.get_text()
last_page=int(int(paper_cnt[:len(paper_cnt)-8])/50)+1

#Scrapping the papers from searched webpage
for offset in range (1,last_page+1):
    print("Page: "+str(offset))
    browser.get(url.format(offset))
    time.sleep(3)
    soup=BeautifulSoup(browser.page_source,"lxml")
    paper_blocks=soup.find_all('li', attrs={'class':'app-article-list-row__item'})
    for paper in paper_blocks:
        cur_doi='10.1038/'+paper.find('a',attrs={'class':'c-card__link u-link-inherit'})['href'][10:]
        try:
            scopus_doi(cur_doi)
        except:
            
            try:
                crossref_doi(cur_doi)
            except:
                print('http://www.nature.com'+paper.find('a',attrs={'class':'c-card__link u-link-inherit'})['href'])
            
f.close()

# +
# 6. RSC

# Change list: keyword

# Change keyword as you want in quatation mark
keyword='all solid state battery'

#Open csv file for data saving
filename=keyword+"_RSC.csv"
f=open(filename,"w",encoding="utf-8-sig", newline="")
writer=csv.writer(f)
head=["Title","Link","Journal","Year","Authors","Affiliations","Countrys"]
writer.writerow(head)

#Find last_page number
url='https://pubs.rsc.org/en/results?searchtext='+keyword_convert(keyword)+'#pnlArticles'
soup=load_page(url)
last_page=int(soup.find('span', attrs={'class':'paging--label'}).get_text()[21:])

#Scrapping the papers from searched webpage
for offset in range (1,last_page+1):
    print("Page: "+str(offset))
    #wait for loading the page
    time.sleep(3)
    soup=BeautifulSoup(browser.page_source,"lxml")
    paper_blocks=soup.find_all('div', attrs={'class':'capsule capsule--article'})
    for paper in paper_blocks:
        try:
            paper_type=paper.find('span', attrs={'class':'capsule__context'}).get_text()
            cur_doi=paper.find('div', attrs={'class':'capsule__footer'}).a['href'][16:]
        except:
            continue
        if ispaper(paper_type):
            try:
                scopus_doi(cur_doi)
            except:
                try:
                    crossref_doi(cur_doi)
                except:
                    print(cur_doi)

    #move to next page if the page is not the last page      
    if offset !=last_page+1:
        browser.find_element_by_xpath('/html/body/main/div[2]/div[3]/div/div[1]/section[2]/div/div[2]/div/div/div[2]/div[1]/nav/ul/li[2]').click()            

f.close()
# -

#test_crossref_doi: print paper_data from Crossref database
test_crossref_doi('10.1021/acsami.1c13541')

#test_scopus_doi: print paper_data from Scopus database
test_scopus_doi('10.1021/acsami.1c13541')

soup=BeautifulSoup(browser.page_source,"lxml")
paper_cnt=soup.find('div', attrs={'class':'fixpadv--l pos--left pagination-summary'}).get_text()
print(paper_cnt[1:6])

results=AbstractRetrieval('10.1021/acsami.1c13541')
print(results)

paper_count('in-situ TEM')
