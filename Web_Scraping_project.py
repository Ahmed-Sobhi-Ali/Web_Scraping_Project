#Cyber Security News Web Scraping Project - by Ahmed Sobhi.
#This Python script scrapes cyber security news from various sources
# and compiles them into an HTML file for easy access.
#you can add any other websites, The code is designed for easy modification and extension.

#importing modules
import os
import requests
import datetime
import pandas as pd
from bs4 import BeautifulSoup

#websites of interest
urls_list = ["https://cybersecuritynews.com/" 
             , "https://www.darkreading.com/"]

#get today's date
def get_date():
    date = datetime.date.today().strftime("%B %d, %Y")
    date = datetime.datetime.strptime(date, "%B %d, %Y")
    return str(date)[0:10]


#get the path, where the file where be extracted
def output_file_path():
    cwt = os.path.dirname(os.path.abspath(__file__))
    return cwt

#send request for each website
def get_request(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content , 'lxml')
    return soup

#get source code for each page
source = list(map(get_request , urls_list))

#extract data from first website
def extract_data1(site , tag , clas):
    raw_data = site.find_all(tag , {'class' : f'{clas}'})
    news = {}

    for data in raw_data:
        title = data.contents[1].find('a').text
        link = data.contents[1].find('a').get('href')
        
        news_date = data.contents[3].find('time').text
        news_date = datetime.datetime.strptime(news_date, "%B %d, %Y")
        news_date = str(news_date)[0:10]
        # check for news date
        if news_date == get_date():
            news.update({title : link})
    return news       
    
news1 = extract_data1(source[0],'div','item-details')

#extract data from second website
def extract_data2(site , tag , clas):
    news = {}
    raw_data = site.find_all(tag , {'class' : f'{clas}'})

    for data in raw_data:
        title = data.text
        link = data.get('href')
        link = f"https://www.darkreading.com{link}"
        news.update({title : link})
    return news       
    
news2 = extract_data2(source[1],"a","ListPreview-Title")

#total news
news1.update(news2)

#extraxt news to html file
def news_to_html(total_news):
    # news data
    data = total_news
    #convert dict to list
    data_list = [[title, f'<a href="{link}" style="color: blue; text-decoration: underline; " target="_blank">{link}</a>'] for title, link in data.items()]

    # design of data frame
    df = pd.DataFrame(data_list, columns=["Title", "Link"])
    df.index += 1
    #HTML and CSS
    html_table = df.to_html(escape=False, classes='styled-table')

    html_table = f'''
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    .styled-table {{
        width: 100%;
        border-collapse: collapse;
        margin: 25px 0;
        font-size: 0.9em;
        font-family: sans-serif;
        min-width: 400px;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
    }}
    .styled-table thead th {{
        padding: 12px 15px;
        text-align: left;
        border-bottom: 1px solid #ddd;
        background-color: #f7f7f9;
        color: #000;
    }}
    .styled-table tbody td {{
        padding: 12px 15px;
        text-align: left;
        border-bottom: 1px solid #ddd;
    }}
    .styled-table tbody tr:nth-of-type(even) {{
        background-color: #f3f3f4;
    }}
    .styled-table tbody tr:last-of-type {{
        border-bottom: 2px solid #009879;
    }}
    .styled-table tbody tr.active-row {{
        font-weight: bold;
        color: #009879;
    }}
    </style>
    </head>
    <body>
    {html_table}
    </body>
    </html>
    '''
    # etract table to html file
    with open(f"{output_file_path()}\\security_news_report.html", "w") as f:
        f.write(html_table)

news_to_html(news1)