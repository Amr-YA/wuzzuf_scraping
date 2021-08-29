#!/usr/bin/env python
# coding: utf-8

# **Imports**

# In[1]:


import requests
import csv
# BeautifulSoup to scrap the basic landing page
from bs4 import BeautifulSoup
# Selenium to scrap the individual job posts, and extract the fields populated by scripts
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# itertools for handling the list of values and transposing
import itertools


# **The Initial Page**

# In[2]:


# The first page of the search result for with search input "python"
URL = 'https://wuzzuf.net/search/jobs/?a=hpb&q=python&start=0'


# **Scraping the search result page**

# In[4]:


# Empty container lists, will be filled with the extracted data
page = 0
companies = []
titles = []
locations = []
skills = []
contracts = []
links = []

# using while loop to iterate through the search pages till there's no more search results
# each loop will extract one page data, and fill the data in the container lists
while True:
    # search result url, changing to match the page number
    page_url = f'{URL[:-1]}{page}'
    
    # Using request and beautiful soup to extract the content of the page
    result = requests.get(page_url)
    result_content = result.content
    soup = BeautifulSoup(result_content, 'lxml')
    
    # The number of total ads found in the search result
    ad_number = int(soup.find('strong').text)

    # Extracting the info from the page soup
    # result: list of html tag with its text
    job_titles = soup.find_all("a", {'class': 'css-o171kl', 'rel': 'noreferrer'})
    location_names = soup.find_all('span', {'class': 'css-5wys0k'})
    contract_type = soup.find_all('div', {'class': 'css-1lh32fc'})
    job_skills = soup.find_all('div', {'class': 'css-y4udm8'})
    company_names = soup.find_all("a", {'class': 'css-17s97q8'})

    page_len = len(company_names)
    
    # populating container lists with the text from info extracted from the page
    # each for loop fills the data for one job post
    for item in range(page_len):
        companies.append(company_names[item].text)
        links.append(job_titles[item].attrs['href'])
        titles.append(job_titles[item].text)
        locations.append(location_names[item].text)
        skills.append(job_skills[item].text)
        contracts.append(contract_type[item].text)
    
    # Iterate through the search result pages
    page += 1
    reached_ad = int(soup.find('li', class_='css-8neukt').text.split()[3])
    print(f'Page: {page}, ads: {reached_ad}')
    
    # Exit the while only when scraped posts number matches the max number of search results
    if reached_ad >= ad_number:
        print('get out')
        break


# **Selenium for extracting salary**

# In[13]:


# Salary field are inside each post page, and is filled using javaScript
# can't be extracted using BeautifulSoup, because the field doesn't have any value from the html page
# have to run through each post page and extract the salary using selenium
# using Option & headless to stop selenium from opening a FireFox window
options = webdriver.FirefoxOptions() 
options.headless= True
driver = webdriver.Firefox(options=options)


# **Sample Salary**  
# since extracting using the selenium is very long process, try extracting just the first item as a proof it works

# In[31]:


salaries = []

for i, link in enumerate(links):
    driver.get(link)    
    # Extract the salary field using selenium find
    salaries.append(driver.find_elements_by_class_name('css-4xky9y')[3].text)

    """    
    # Or we can use soup since we already have the driver with page data filled in
    # Extract the salary field using soup find 
    soup = BeautifulSoup(driver.page_source, 'lxml')
    print(soup.find_all("span", class_='css-4xky9y')[3].text)
    """

    # Break to extract only sample of the 4 link
    # remove the break when extracting all the data
    if i == 3:
        break
driver.quit()


# **Creating the CSV file**

# In[36]:


# Header and row values list
col_names = ['Title', 'Company', 'Location', 'Contract', 'Skills', 'Link', 'Salaries']
col_values = [titles, companies, locations, contracts, skills, links, salaries]

# transpose the values list (initial col_values would have each row with the same data)
# ex from col_values: 1st row all titles, 2nd row all companies
# we want the result to be one value type in each cell of the row, ex: 1st row: 1 title, 1 company, 1 loc ....
# using itertools and zip_longest to transpose and handle missing values in the same time
col_values2 = list(map(list, itertools.zip_longest(*col_values, fillvalue='not fetched')))

# Write the list of values in a CSV file
with open('jobs.csv', 'w', newline = '', encoding='UTF8') as f:
    wr = csv.writer(f)
    wr.writerow(col_names)
    wr.writerows(col_values2)
print('file created')


# In[ ]:




