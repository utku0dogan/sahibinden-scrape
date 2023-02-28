from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pandas as pd


root = 'https://www.sahibinden.com/'

headers = {
        'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)' +
        'AppleWebKit/537.36 (KHTML, like Gecko)' +
        'Chrome/39.0.2171.95 Safari/537.36',
        'Upgrade-Insecure-Requests': '1'}

# dict = {
# "marka": "audi",
# "model":"a3 a3 hatchback",
# "il": "istanbul",
# "vites":"manuel",
# "yil":{
#     "max":"2023",
#     "min": "2000"
# },
# "price":{
#     "min":"1",
#     "max":"10000000"
# }

# }
def createURL(dict):
    modelURL = (root + dict['marka'] + '-' + dict['model']).replace(' ','-')
    yilquery = 'a5min=' + dict['yil']['min'] + '&' +  'a5max=' + dict['yil']['max']
    pricequery= 'price_min=' + dict['price']['min'] + '&' + 'price_max=' + dict['price']['max']
    queries = '?'+yilquery+pricequery
    pages = modelURL + '/'+dict['il']+'/'+dict['vites']
    URL = pages + queries
    return URL


def get_pagecount(URL):
    r = requests.get(URL, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    print('response: ' + str(r.status_code))
    sayfa_sayisi = int(soup.find('div',{'class':'mtmdef pageNavigator pvdef phdef'}).get_text().split()[1])
    return sayfa_sayisi


def scrape(dict):
    ilanlar = []
    URL = createURL(dict)
    sayfa_sayisi = get_pagecount(URL)
    for offset in range(0, sayfa_sayisi*20, 20):
        try:
          offset = '&pagingOffset='+str(offset)
          URL_ = URL + offset
          # start scraping the page
          r = requests.get(URL_, headers=headers)
          print(r.status_code, URL_)
          soup = BeautifulSoup(r.text, 'html.parser')
          for i in soup.find_all('tr', {'class':'searchResultsItem'}):
              temp=[]
              if i.find('td', {'class':'searchResultsLocationValue'}):
                  temp.append(i.find('td', {'class':'searchResultsLocationValue'}).get_text(separator = ' ').replace('\n','').replace('\r', '').replace('\t', '').strip())
              if i.find('td',{'class':'searchResultsTagAttributeValue'}):
                  temp.append(i.find('td', {'class':'searchResultsTagAttributeValue'}).get_text(separator = ' ').replace('\n','').replace('\r', '').replace('\t', '').strip())
              if i.find('td',{'class':'searchResultsAttributeValue'}):
                  for j in i.find_all('td',{'class':'searchResultsAttributeValue'}):
                      temp.append(j.get_text(separator = ' ').replace('\n','').replace('\r', '').replace('\t', '').strip())
              if len(temp) > 0:
                  ilanlar.append(temp)
        except Exception as e:
          print("Exception occured: " + str(e))
          continue

    
    return saveData(ilanlar)


def saveData(ilanlar):
    df = pd.DataFrame(ilanlar, columns = ['konum', 'model','model_yil','km','renk'])
    out = df.to_json(orient='records',force_ascii=False)
    with open('ilanlar.json', 'w') as f:
        f.write(out)
    return out

if __name__ == "__main__":
	scrape(dict)
