from scrapping_libs import get_detail_data, load_pkl, dump_pkl, get_all_rel_links_dates_minmax_price

satellite = ['tangerang',
             'tangerang-selatan',
             'depok',
             'bekasi']

dki = ['jakarta-utara',
       'jakarta-selatan',
       'jakarta-barat',
       'jakarta-timur',
       'jakarta-pusat']

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0'
}

minprice = 300000000
maxprice = 800000000

for city_name in satellite:
    get_all_rel_links_dates_minmax_price(city_name, minprice, maxprice)
    
for city_name in dki:
    get_all_rel_links_dates_minmax_price(city_name, minprice, maxprice, header)