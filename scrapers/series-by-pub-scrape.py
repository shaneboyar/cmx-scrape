# Import libraries
import requests
import time
import csv
import helpers
import random
from bs4 import BeautifulSoup


slugs = ['1-0', '2-0', '4-0', '12-0', '3-0', '5-0', '18-0', '9-0', '94-0', '11-0', '47-0', '53-0', '8-0', '99-0', '96-0', '7816-0', '8-21', '18-0', '18-61', '64-0', '4-7', '808-0', '9776-0', '128-0', '14-0', '12-118', '48-0', '1-3']

with open('../scrapes/series-by-pub.csv', 'a') as csv_file:
  writer = csv.writer(csv_file)
  writer.writerow(['series title', 'series link'])

for slug in slugs:
  page_number = 1
  # specify the url
  series_page = 'https://www.comixology.com/series/comics-publisher/' + slug
  # query the website and return the html to the variable 'page'
  page = requests.get(series_page)
  # parse the html using beautiful soup and store in variable 'soup'
  soup = BeautifulSoup(page.content, 'html.parser')
  publisher_name = soup.find('h2', class_="hinline").text.strip()
  pub_series_list = soup.find(class_="seriesList")

  count = soup.find(class_='pager-jump-container') # TODO: Check this for bundles > 5 pages
  page_count_for_pub = int(count.text.strip().replace(u'Jump to:\n / ','')) if count else helpers.find_page_count_by_paginators(soup)

  series_details_list = pub_series_list.find_all(class_='content-img-link')

  while page_number <= page_count_for_pub:
    time.sleep(1)
    series_list = []
    print('Grabbing comics from ' + publisher_name + '. Page ' + str(page_number))
    if page_number > 1:
      series_page = 'https://www.comixology.com/series/comics-publisher/' + slug + '?seriesList_pg=' + str(page_number)
      page = requests.get(series_page)
      soup = BeautifulSoup(page.content, 'html.parser')
      pub_series_list = soup.find(class_="seriesList")
      series_details_list = pub_series_list.find_all(class_='content-img-link')
    if len(series_details_list):
      for series_details in series_details_list:
        series = {}
        name = series_details.contents[1].attrs['title'].strip() # strip() is used to remove starting and trailing
        series['title'] = name.replace(u'\xc0', u'').replace('  ', '')
        series['link'] = series_details.attrs['href'].replace('  ', '').split('?', 1)[0]
        series_list.append(series)
      # open a csv file with append, so old data will not be erased
      print(series_list)
      with open('../scrapes/series-by-pub.csv', 'a') as csv_file:
        writer = csv.writer(csv_file)
        for series in series_list:
          writer.writerow([series['title'], series['link']])
    page_number += 1
