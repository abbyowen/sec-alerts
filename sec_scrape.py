#!/usr/bin/env python
#Author: Abby Owen
#Purpose: Create a web scraper that will send a message to my friend Ray each day
#letting her know if there are any new listings of Golden Goose shoes available

import requests
from bs4 import BeautifulSoup
from Ticker import Ticker
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
#import schedule
#import time
#from twilio.rest import Client
#import datetime

# URL to scrape
url = 'http://openinsider.com/screener?s=&o=&pl=&ph=&ll=&lh=&fd=14&fdr=&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xp=1&vl=&vh=50&ocl=&och=&sic1=-1&sicl=100&sich=9999&grp=2&nfl=&nfh=&nil=2&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=100&page=1'

# File that keeps track of the listings that my system "knows about" so it can
# distinguish between new and old listings
old_filings = 'sec_filings.txt'

email = "elizabeth.l.orecchia@gmail.com"

# I use cronitor to manage my cron jobs so I get notified if there are any
# errors if the code doesn't run at 12:00 as it should
#requests.get(
  # 'https://cronitor.link/HzlGgI/run',
  # timeout=10
#)

# Returns the number of lines in my file
def check_file_lines(filename):
    file = open(filename, 'r')
    lines = 0
    for line in filename:
        lines = lines + 1
    file.close()
    return lines


# Establish a base for the first run of the scraper
# Creates a csv file of the listings on the first pass
def base_filings(url, filename):

    file = open(filename, 'r+')

    # Flag myself as a User-Agent to allow access to the page as a scraper
    headers = {'User-Agent': 'APIs-Google (+https://developers.google.com/webmasters/APIs-Google.html)'}

    # Get the page to scrape
    page = requests.get(url, headers=headers)

    print("success")

    # Use Beautiful Soup to parse the HTML of the page
    soup = BeautifulSoup(page.content, 'html.parser')
    #print(soup)
    table = soup.find('table', {'class': "tinytable"})
    headers = table.find("thead")
    fields = headers.find_all('h3')
    for field in fields:
        print(field.text)
    rows = table.findChildren(['th','tr'])
    #print(rows)
    tickers = []
    for row in rows:
        print("---------------------")
        cells = row.findChildren('td')
        info = []
        for cell in cells:
            info.append(cell.text)
        if len(info) != 0:
            filing_date, trade_date, ticker, company, industry, ins, trade_type, price, qty, owned, delta_own, value = info[1:13]
            new_ticker = Ticker(filing_date, trade_date, ticker, company, industry, ins, trade_type, price, qty, owned, delta_own, value)
            print(new_ticker)
            tickers.append(new_ticker)
    
    
    if os.stat(filename).st_size == 0:
        for ticker in tickers:
            file.write(ticker.txt_row() + "\n")

    file.close()
    return tickers

def new_filings(url, filename):
    
    file = open(filename, 'r+')
    check_filings = base_filings(url, filename)
    
    latest_time = datetime.strptime(file.readline().split(',')[0], '%Y-%m-%d %H:%M:%S')
    new_filing_date = datetime.strptime(check_filings[0].filing_date, '%Y-%m-%d %H:%M:%S')
    print(latest_time)
    print(new_filing_date)
    i = 0
    new_filings = []
    while new_filing_date > latest_time:
        new_filings.append(check_filings[i])
        i += 1
        new_filing_date = datetime.strptime(check_filings[i].filing_date, '%Y-%m-%d %H:%M:%S')
    print(new_filings)
    
    file.close()
    
    if len(new_filings) > 0:
        file = open(filename, 'w')
        for filing in new_filings:
            file.write(filing.txt_row() + "\n")
        notify(new_filings, email)
        file.close()
    

def notify(body, email):
    html = "<h2>New filings have been made.</h2>"
    for ticker in body:
        t_str = str(ticker)
        print(type(t_str))
        t_str.split("\n")
        '<br>'.join(t_str)
        add = "<p>" + t_str + "</p>"
        html += add
    
    print(html)
    message = Mail(
    from_email='abbyhaowen@gmail.com',
    to_emails=email,
    subject='NEW SEC FILING ALERT',
    html_content=html)
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        print(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)
        print(e.body)

new_filings(url, old_filings)


