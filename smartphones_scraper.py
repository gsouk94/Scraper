#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import necessary libraries

from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from selenium import webdriver


# In[2]:


phone_list = [] # create an empty list
driver = webdriver.Firefox()
driver.get('https://www.skroutz.gr/c/40/kinhta-thlefwna/f/852219/Smartphones.html?o=smartphone&page=') # the link we want to scrape

def scrape(url, page, stop): # define a scraping function
    
    
    while page != None:
        html = driver.page_source
        soup = bs(html, "lxml")
        cards = soup.findAll('li', {'class': 'cf card with-skus-slider'})
    
        for phone in cards:
            phone = {
                'product_name': phone.div.h2.a.text,
                'price': (phone.findAll('div', {'class': 'price react-component reviewable'})[0].div.a.text.replace(",", ".")),
                'specs': phone.findAll('p', {'class': 'specs'})[0].text.replace(",", " "),
                'rating': float(phone.findAll('a', {'class': 'rating stars'})[0].span.text),
                'stores' :phone.findAll('span', {'class': 'shop-count'})[0].text,
                'reviews' :phone.findAll('div', {'class': 'reviews-count'})[0].text
            }
            phone_list.append(phone)
        
        if page == stop:
            break
        page = page + 1
    


# In[7]:


scrape('https://www.skroutz.gr/c/40/kinhta-thlefwna/f/852219/Smartphones.html?page={page}', 1,34) # Scrape webpages


# In[8]:


df = pd.DataFrame.from_dict(phone_list) # Create a pandas dataframe from our dictionary


# In[9]:


df.shape # Check the number of observations we scrapped


# In[6]:


df.head() # let's check our dataset


# In[10]:


pd.set_option('display.max_colwidth', None) # Display all characters of strings
df.head()


# In[11]:


import re # Import re for writing regular expressions and clean the dataset from greek characters

df['ram'] = df['product_name'].str.extract(r'(\(.*/)')
df['rom'] = df['product_name'].str.extract(r'(/.*\))')
df['name'] = df["product_name"].str.extract(r'([a-zA-Z].*\()')
df['stores'] = df["stores"].str.extract(r'(\d\d)')
df['price'] = df['price'].str.extract(r'(\d.*\d)')
df['year'] = df["specs"].str.extract(r'(:.*\d)')
df['screen'] = df["specs"].str.extract(r'(η:.*")')
df['inches'] = df['screen'].str.extract(r'(\d.*\d)')
df['screen'] = df['screen'].str.replace((r'(\d.*\d)'), "")


# In[12]:


df.screen = df['screen'].str.replace("η|:", "") # Clean screen column

df["screen"] = df["screen"].str.replace(r'( ")', "")


# In[13]:


df["ram"] = df["ram"].str.extract(r'(\d)') # Clean ram column 


# In[14]:


df['rom'] = df['rom'].str.extract(r'(\d.*\d)') # clean rom column 


# In[15]:


df['name'] = df['name'].str.replace(r'(\()', "") # clean name column


# In[16]:


# Clean year column
    
df['year'] = df['year'].str.extract(r'(\d.*η)') # Clean year column
df['year'] = df['year'].str.extract(r'(\d.*\d)')

# Clean price column
df["price"] = df['price'].str.replace(".", "") # remove separator
pd.to_numeric(df["price"]) # tranfrom to numeric and then to float
df['price'] = df['price'].astype(float)
df['price'] = df['price'].div(100) # divide the prices with 100 to get the original price


# In[17]:


# Clean battery column

df['battery'] = df['specs'].str.extract(r'(α.*h)') # Clean battery column
df['battery'] = df['battery'].str.replace("αταρία:", "")
df['battery'] = df['battery'].str.replace("mAh", "")


# In[18]:


# Drop columns that we do not need

df.drop(["specs"], axis = 1, inplace = True)
df.drop(["product_name"], axis = 1, inplace = True)


# In[19]:


# Reorder the columns

df = df[["name", "price", "rating", 'reviews', "stores", "year", "ram", "rom", "screen", "inches", "battery" ]] 


# In[20]:


# Check columns types

df.dtypes 


# In[22]:


# Create a brand column 

df['brand'] = df['name'].apply(lambda x: x.split(' ')[0])


# In[23]:


# Format data types

df['ram'] = df['ram'].astype(int)
pd.to_numeric(df["rom"])
df['inches'] = df['inches'].astype(float)
df['battery'] = df['battery'].fillna(0)
df['battery'] = df['battery'].astype(int)
df['rom'] = df['rom'].astype(int)


# In[24]:


# Turn brand and screen columns into lowercase

df['brand'] = df['brand'].str.lower()
df['screen'] = df['screen'].str.lower()


# In[25]:


# Import other useful libraries

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


# In[26]:


df.head()


# In[27]:


# Our dataset is now clean. We created the necessary columns and we are ready for analysis. 
# For example we could start with some simple graphs or simple descriptice statistics
# Which brands have the larger amount of models in the market?

sns.catplot(x = 'brand', kind = 'count', data = df)


# In[35]:


## We can group our dataset by different columns
phones = df.groupby('brand')
phones.first()


# In[30]:


## Group our dataset by a specific brand 

phones.get_group('xiaomi')


# In[ ]:


## Now that our dataset is ready we can explore the data and give answers to our questions

