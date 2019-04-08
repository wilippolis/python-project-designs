from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import urllib.request, urllib.parse, requests, re
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as Soup
from selenium import webdriver
from time import sleep
import pprint
import sys

class Client(object):

    def __init__(self, url):
        option = webdriver.ChromeOptions()
        option.add_argument('-incognito')
        browser = webdriver.Chrome(
            executable_path='C:/Users/wilip/Downloads/chromedriver_win32/chromedriver.exe',
            chrome_options=option
        )
        browser.get(url)
        sleep(5)
        self.source = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")

    def __repr__(self):
        return repr(self.source)

    # Causes Key
#   Animals: 33
#   Ars & Culture: 34
#   Black Male Achievement: 46
#   Civil Rights: 35
#   Community & Economic Development: 45
#   Disaster Relief: 41
#   Disease & Medical Research: 42
#   Education: 8
#   Employment Services: 43
#   Environment: 9
#   Health & Nutrition: 40
#   Housing & Homelessness: 13
#   Human Services: 37
#   International Affairs: 21
#   Justice & Legal Services: 36
#   LGBT: 48
#   Maternal Health: 47
#   Philanthropy & Capacity Building: 39
#   Religion & Spirituality: 38
#   Science & Technology: 29
#   Violence Prevention: 49
#   Women's Issues: 27
#   Youth Development: 44
    
def scrape(cause, pages):

    all_companies = []
    url = 'https://www.catchafire.org/volunteer/?init=1&type_filter=2&type_filter=1&cause_filter='+cause+'&skill_filter=2&skill_filter=21&skill_filter=19&skill_filter=27&skill_filter=4&skill_filter=28&skill_filter=29&skill_filter=24&skill_filter=37&skill_filter=26&skill_filter=6&skill_filter=16&skill_filter=5&skill_filter=7&skill_filter=30&skill_filter=35&skill_filter=31&skill_filter=9&skill_filter=11&skill_filter=12&skill_filter=36&skill_filter=13&skill_filter=14&skill_filter=33&skill_filter=34&skill_filter=23&search=1'


    for page in range(1, pages + 1):

        if cause != '':
            if page == 1:
                url = 'https://www.catchafire.org/volunteer/?init=1&type_filter=2&type_filter=1&cause_filter='+cause+'&skill_filter=2&skill_filter=21&skill_filter=19&skill_filter=27&skill_filter=4&skill_filter=28&skill_filter=29&skill_filter=24&skill_filter=37&skill_filter=26&skill_filter=6&skill_filter=16&skill_filter=5&skill_filter=7&skill_filter=30&skill_filter=35&skill_filter=31&skill_filter=9&skill_filter=11&skill_filter=12&skill_filter=36&skill_filter=13&skill_filter=14&skill_filter=33&skill_filter=34&skill_filter=23&search=1'
            else:
                url = 'https://www.catchafire.org/volunteer/?page='+str(page)+'&type_filter=2&type_filter=1&cause_filter='+cause+'&skill_filter=2&skill_filter=21&skill_filter=19&skill_filter=27&skill_filter=4&skill_filter=28&skill_filter=29&skill_filter=24&skill_filter=37&skill_filter=26&skill_filter=6&skill_filter=16&skill_filter=5&skill_filter=7&skill_filter=30&skill_filter=35&skill_filter=31&skill_filter=9&skill_filter=11&skill_filter=12&skill_filter=36&skill_filter=13&skill_filter=14&skill_filter=33&skill_filter=34&skill_filter=23&search=1'

        else:
            print('Catchafire scraper requires a cause input')
            
        print(url)

    source = Client(url).source
    soup = Soup(source,'lxml')
    results = soup.findAll('div', attrs={'class':'card text-center project'})
    print(results)
    for result in results:
        d = {'source':'catchafire', 'is_company': False}

        try:
            body = result.find('div', attrs={'class':'card-block'})
            d['type'] = body.find('h4').get_text().strip()
            d['offsiteURL'] = "https://www.catchafire.org" + body.find('h4').find('a').attrs['href']
            d['title'] = body.find('h5').find('a').get_text().strip()
            d['duration'] = body.find('p').get_text().strip()
            footer = result.find('div', attrs={'class':'card-footer'})
            d['company'] = footer.find('h6').find('a').get_text().strip()
            d['companyLink'] = "https://www.catchafire.org" + footer.find('h6').find('a').attrs['href']
            d['category'] = footer.find('p').find('a').get_text().strip()
        except Exception as e:
            print(e)

        if 'title' in d.keys():
            all_companies.append(d)
                
    return all_companies

pprint.pprint(scrape('35',2))
