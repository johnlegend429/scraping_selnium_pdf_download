#!/usr/bin/env python
# coding: utf-8

# In[1]:

########################### PART 1 ############################
#import the library used to query a website
import urllib.request
import pandas as pd
from urllib.parse import urljoin
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from config import forAuthor

mainUrl= forAuthor
driver= webdriver.Chrome()
driver.get(mainUrl)
links= driver.find_elements(By.TAG_NAME, 'a')
#source
published= driver.find_element(By.TAG_NAME, 'h4')
Heading= published.text.strip()
last_part = Heading.split('(')[-1]
source = last_part.rstrip(')').strip()
n = 0
result= []
for link in links:
    urlpdf= link.get_attribute("href")
    n = n+1
    if n> 4 : 

        url=urlpdf
            
        #Query the website and return the html to the variable 'page'

        driver = webdriver.Chrome()
        driver.get(url)


        all_link= driver.find_elements(By.TAG_NAME, 'a')
        A=[]
        B=[]
        for link in all_link:
            # append the link text to A
            A.append(link.text)
            # append the absolute URL of the link to B
            href = link.get_attribute('href')
            B.append(urljoin(url, href))

        df = pd.DataFrame({
            'Description': A,
            'Link': B
        })
        dirname = os.path.dirname(__file__)
        #dirname="C:\py\crawler"
        relpath='output'
        path= os.path.join(dirname, relpath,"output.csv")

        h4 = driver.find_element(By.TAG_NAME, 'h4')
        name = h4.text.strip()
        result.append(name) 
        print(result)
        # df1 = pd.DataFrame({
        #     'PdfName': [name],
        #     'path': "/code/output"
        # })
        # dirname = os.path.dirname(__file__)
        # route= os.path.join(dirname, relpath,"Pdf.csv")
        # df1.to_csv(route)

        for link in B:
            file_name = f"{name}.pdf"
            print("start with ",file_name)


            #test if link is open
            try: u=urllib.request.urlopen(link)
            except urllib.error.URLError as e:
                print(e.reason)
                continue
            
            #determine file name end with .pdf, skip this file otherwise
            meta = u.info()
            if(meta['Content-Type']!='application/pdf'):
                print(file_name," is not a PDF file")
                continue
                
            #set abosolute path for the file
            path_file_name = os.path.join(dirname, relpath,file_name)
            print("path_file_name is",path_file_name)
                
            #download file  
            f = open(path_file_name, 'wb')
            file_size=int(meta['Content-Length'])
            print (f"Downloading: %s Bytes: %s" % (file_name, file_size))
            file_size_dl = 0
            block_sz = 8192
            while True:
                buffer = u.read(block_sz)
                if not buffer:
                    break
                file_size_dl += len(buffer)
                f.write(buffer)
            print("downloading finished")
        df= pd.DataFrame(result, columns=['Title'])
        df.to_csv('/code/output/{}.csv'.format(source), index=False)    
    
        f.close()


        # In[ ]:




