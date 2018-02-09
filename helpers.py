def find_page_count_by_paginators(soup):
  count = soup.find_all(class_='pager-link')
  return int(count[len(count) - 2].attrs['data-page']) if count else 1

def series_section_page_count(soup, section_name):
  section = soup.find(class_=section_name)
  if section == None:
    return 0
  count = section.find(class_='pager-jump-container')
  return int(count.text.strip().replace(u'Jump to:\n / ','')) if count else find_page_count_by_paginators(section)