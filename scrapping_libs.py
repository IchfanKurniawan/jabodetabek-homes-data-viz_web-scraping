from requests_html import HTMLSession
import requests
from bs4 import BeautifulSoup as bs
import json
import pickle
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry    


# all the data is scrapped from: rumah123.com

def get_page_max(url_base, header):
    """
    input: base url of rumah123 dot com
    output: page maximum
    """
    r = requests.get(url_base, headers=header)
    soup = bs(r.content, 'lxml')
    num_pages = [ int(li.get_text(strip=True)) for li in soup.find_all('li', class_='ui-molecule-paginate__item')]
    return(num_pages[-1])

def get_link_date(url, header):
    """ 
    input: url of rumah 123 dot com
    output: relative link of each home in each page
    """
    r = requests.get(url, headers=header)
    soup = bs(r.content, 'lxml')
    a_tag = [i.find('a', class_='ui-organisms-card-r123-featured__middle-section__title', href=True) for i in soup.find_all('div', class_='ui-organisms-card-r123-featured__middle-section')]
    rel_links = [a['href'] for a in a_tag]
    
    agent = [i.find_all('p') for i in soup.find_all('div', class_='ui-organisms-card-r123-basic__bottom-section__agent')]
    date = [i[-1].text for i in agent]
    
    return (rel_links, date)

def dump_pkl(file, dump_name):
    with open(dump_name, 'wb') as f:   
        pickle.dump(file, f)
    return None

def load_pkl(load_name):
    import pickle
    with open(load_name, 'rb') as f:
        file = pickle.load(f)
    return file

def get_all_rel_links_dates(city_name, header):
    """ 
    input: None
    output: a pickle file contains all relative links & dates from rumah123dotcom for all homes in jakarta
    """
    print(f'data for: city {city_name}')
    url_base = f'https://www.rumah123.com/jual/{city_name}/rumah/?page=1#qid~6968d3a1-8458-458e-b8f9-03a70f850b26'
    
    
    all_data = []
    max_page = get_page_max(url_base, header)
    print('max page: ' + str(max_page))

    for num_page in range(1, max_page+1):
        url = f'https://www.rumah123.com/jual/{city_name}/rumah/?page={num_page}#qid~6968d3a1-8458-458e-b8f9-03a70f850b26'
        page_rel_links, date_given = get_link_date(url)
        
        for i in range(0, len(page_rel_links)):
            all_data.append([page_rel_links[i], date_given[i]])
        
        dump_pkl(all_data, f'.\\pickle\\link_date_rumah123_{city_name}.pkl')
        if num_page%10==0: 
            print(f'num page: {num_page} saved ({city_name})')
        
        time.sleep(1.5)
        
    print('all data saved!')
    return None

def get_detail_data(rel_link_date, header):
    """ 
    input: list of link & date
    output: dictionary of rellink, date, price, etc.
    """
    
    base = 'https://www.rumah123.com'
    url_home = base + rel_link_date[0]
    date = rel_link_date[1]
    rellink = rel_link_date[0]
    
    r = requests.get(url_home, headers=header)
    
    
    soup = bs(r.content, 'html.parser')
    # date = # take from tuple index
    try:
        title = soup.find('div', class_='r123-listing-summary__header-container-title').get_text(strip=True)    
    except Exception as e:
        title = ''
    
    try:
        price = soup.find('div', class_='r123-listing-summary__price').get_text(strip=True)    
    except Exception as e:
        price = ''
        
    try:
        installment = soup.find('div', class_='r123-listing-summary__installment').get_text(strip=True)    
    except Exception as e:
        installment = ''
        
    try:
        address = soup.find('div', class_='r123-listing-summary__header-container-address').get_text(strip=True)    
    except Exception as e:
        address = ''
        
    
            

    property_data = {
        'title': title
        , 'price': price
        , 'installment': installment
        , 'address': address
        , 'date': date
        , 'rel_link': rellink 
    }

    try:
        description = soup.find('div', class_='sc-breuTD gBGXJv').get_text(strip=True).replace('Deskripsi', '')    
    except Exception as e:
        description = ''
    
    try:
        facilities = [ facility.get_text(strip=True) for facility in soup.find_all('div', class_='ui-facilities-portal__item')]
        facilities = ', '.join(facilities)    
    except Exception as e:
        facilities = ''
    
    property_data['facilities'] = facilities
    property_data['description'] = description


    try:
        key_item_additional = [ i.find_all('p') for i in soup.find_all('div', class_='ui-molecule-poi__item')]
        for keyitem in key_item_additional:
            property_data[keyitem[0].get_text(strip=True)] = keyitem[-1].get_text(strip=True)
    except Exception as e:
        None

    # Property Information
    try:
        badges = soup.find('div', class_='ui-listing-specification__badge-wrapper')

        child_list = []
        for child in badges.children:
            child_list.append(child)
            
        ps = [div.find_all('p') for div in child_list]
        for item in ps:
            property_data[item[0].get_text(strip=True)] = item[1].get_text(strip=True)
    except Exception as e:
        None
        
    time.sleep(1) 
    return property_data    

def get_all_rel_links_dates_minmax_price(city_name, minprice, maxprice, header):
    """ 
    input: None
    output: a pickle file contains all relative links & dates from rumah123dotcom for all homes in jakarta
    """
    print(f'data for: city {city_name}')
    url_base = f'https://www.rumah123.com/jual/{city_name}/rumah/?page=1#qid~6968d3a1-8458-458e-b8f9-03a70f850b26'
    
    
    all_data = []
    max_page = get_page_max(url_base)
    print('max page: ' + str(max_page))

    for num_page in range(1, max_page+1):
        url = f'https://www.rumah123.com/jual/{city_name}/rumah/?minPrice={minprice}&maxPrice={maxprice}&page={num_page}#qid~6968d3a1-8458-458e-b8f9-03a70f850b26'
        page_rel_links, date_given = get_link_date(url)
        
        for i in range(0, len(page_rel_links)):
            all_data.append([page_rel_links[i], date_given[i]])
        
        dump_pkl(all_data, f'.\\pickle\\link_date_rumah123_{city_name}_minmaxprice.pkl')
        if num_page%10==0: 
            print(f'num page: {num_page} saved ({city_name}) minmaxprice')
        
        time.sleep(1.5)
        
    print('all data saved!')
    return None
