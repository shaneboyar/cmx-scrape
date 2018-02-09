# Import libraries
import requests
import time
import csv
import pandas
import helpers
from bs4 import BeautifulSoup


# colnames = ['series_title', 'series_link']
# data = pandas.read_csv('comics.csv', names=colnames)

# SERIES_LINKS = data.series_link.tolist()
# SERIES_LINKS.pop(0)

SERIES_LINKS = ['https://www.comixology.com/Zero/comics-series/11427', 'https://www.comixology.com/Batman-1940-2011/comics-series/177']
LIST_TYPES = ['Omnibuses', 'CollectedEditions', 'Issues', 'GraphicNovels', 'OneShots']

with open('series-issues.csv', 'a') as csv_file:
  writer = csv.writer(csv_file)
  writer.writerow(['series title', 'issue title', 'issue link'])

for series_link in SERIES_LINKS:
  # query the website and return the html to the variable 'page'
  page = requests.get(series_link)
  # parse the html using beautiful soup and store in variable 'soup'
  soup = BeautifulSoup(page.content, 'html.parser')

  series_name = soup.find('h2', class_="hinline").text.strip()
  omnibus_page_count = helpers.series_section_page_count(soup, LIST_TYPES[0])
  collection_page_count = helpers.series_section_page_count(soup, LIST_TYPES[1])
  issue_page_count = helpers.series_section_page_count(soup, LIST_TYPES[2])
  page_counts = {LIST_TYPES[0]: omnibus_page_count, LIST_TYPES[1]: collection_page_count, LIST_TYPES[2]: issue_page_count}
  issue_list = []

  print("Scraping " + series_name + ".")

  for list_type in LIST_TYPES:
    if page_counts[list_type] > 0:
      print("Scraping " + list_type + ".")
      page_number = 1
      while page_number <= page_counts[list_type]:
        time.sleep(1)
        link = series_link + "?" + list_type + "_pg=" + str(page_number)
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')
        section = soup.find(class_=list_type)
        issue_content_list = section.find_all(class_="content-img-link")
        if len(issue_content_list):
          for issue_content in issue_content_list:
            if 'title' in issue_content.contents[1].attrs:
              issue = {}
              issue['series_title'] = series_name
              issue['issue_title'] = issue_content.contents[1].attrs['title'].replace('  ', '')
              issue['link'] = issue_content.attrs['href'].split('?', 1)[0]
              issue_list.append(issue)
        page_number += 1
    else:
      print("No " + list_type + ".")
  # open a csv file with append, so old data will not be erased
  with open('series-issues.csv', 'a') as csv_file:
    writer = csv.writer(csv_file)
    for issue in issue_list:
      writer.writerow([issue['series_title'], issue['issue_title'], issue['link']])
