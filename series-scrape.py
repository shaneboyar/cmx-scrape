# Import libraries
import requests
import time
import csv
import helpers
import random
from bs4 import BeautifulSoup


SELECTORS = ['FEATURED', '%23', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

with open('comics.csv', 'a') as csv_file:
  writer = csv.writer(csv_file)
  writer.writerow(['series title', 'series link'])

for selector in SELECTORS:
  time.sleep(random.randint(1,5))
  page_number = 1
  # specify the url
  series_page = 'https://www.comixology.com/browse-series?seriesList_alpha=' + selector + '&seriesList_pg=' + str(page_number) + '&cu=0'
  # query the website and return the html to the variable 'page'
  page = requests.get(series_page)
  # parse the html using beautiful soup and store in variable 'soup'
  soup = BeautifulSoup(page.content, 'html.parser')

  count = soup.find(class_='pager-jump-container')
  page_count_for_selector = int(count.text.strip().replace(u'Jump to:\n / ','')) if count else helpers.find_page_count_by_paginators(soup)


  series_details_list = soup.find_all(class_='content-details')

  while page_number <= page_count_for_selector:
    series_list = []
    time.sleep(1)
    print('Grabbing comics from ' + selector + '. Page ' + str(page_number))
    if page_number > 1:
      series_page = 'https://www.comixology.com/browse-series?seriesList_alpha=' + selector + '&seriesList_pg=' + str(page_number) + '&cu=0'
      page = requests.get(series_page)
      soup = BeautifulSoup(page.content, 'html.parser')
      series_details_list = soup.find_all(class_='content-details')
    if len(series_details_list):
      for series_details in series_details_list:
        series = {}
        name = series_details.text.strip() # strip() is used to remove starting and trailing
        series['title'] = name.replace(u'\xc0', u'').replace('  ', '')
        series['link'] = series_details.attrs['href'].replace('  ', '').split('?', 1)[0]
        series_list.append(series)
      # open a csv file with append, so old data will not be erased
      with open('comics.csv', 'a') as csv_file:
        writer = csv.writer(csv_file)
        for series in series_list:
          writer.writerow([series['title'], series['link']])
    page_number += 1
