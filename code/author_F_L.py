
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from config import forAuthor

#Get urls for Author DATA Scraping

mainUrl= forAuthor
driver= webdriver.Chrome()
driver.get(mainUrl)

# Heading
published= driver.find_element(By.TAG_NAME, 'h4')
Heading= published.text.strip()

#datepublished
year = Heading.split()[-1].replace(')', '')

#source
last_part = Heading.split('(')[-1]
source = last_part.rstrip(')').strip()


all_author= list(driver.find_elements(By.TAG_NAME, 'i'))
n = 0
finalData=[]
for paperAuthor in all_author:
    parent= paperAuthor.find_element(By.XPATH,('..'))
    paperTitle= parent.find_elements(By.XPATH, "//a[@title='paper title']")
    paperAuthorText= paperAuthor.text
    authors= paperAuthorText.split(",")
    for author in authors:
        n = n+1
        if n>5:
            author= author.strip()
            paper_author_index = all_author.index(paperAuthor)
            if author == authors[0].strip() and author != authors[-1].strip():
                data= []
                data.append(author)
                data.append("Yes")
                data.append("No")
                real_title_list = paperTitle[(paper_author_index)-5]
                data.append(real_title_list.text.strip())
                data.append(year)
                # this part is for category
                if "conference" in parent.get_attribute("class"):
                    data.append("Main Conference Track")
                else:
                    data.append("Datasets and Benchmarks Track")
                data.append(source)
            elif author != authors[0].strip() and author == authors[-1].strip():
                data= []
                data.append(author)
                data.append("No")
                data.append("Yes")
                real_title_list = paperTitle[(paper_author_index)-5]
                data.append(real_title_list.text.strip())
                data.append(year)
                if "conference" in parent.get_attribute("class"):
                    data.append("Main Conference Track")
                else:
                    data.append("Datasets and Benchmarks Track")
                    break
                data.append(source)
            else:
                data= []
                data.append(author)
                data.append("No")
                data.append("No")
                real_title_list = paperTitle[(paper_author_index)-5]
                data.append(real_title_list.text.strip())
                data.append(year)
                if "conference" in parent.get_attribute("class"):
                    data.append("Main Conference Track")
                else:
                    data.append("Datasets and Benchmarks Track")
                data.append(source)
            print(data)
            finalData.append(data)
            df = pd.DataFrame(finalData, columns=['Author', 'First Author', 'Last Author', 'Title', 'Year', 'Category', 'Source'])
            df.to_csv('./output_author/{}.csv'.format(Heading), index=False)
                        
