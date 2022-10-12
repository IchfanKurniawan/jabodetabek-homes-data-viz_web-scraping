import pandas as pd
import numpy as np
import regex as re
from datetime import datetime
from scrapping_libs import load_pkl
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="Geolat")
def get_lon(x):
    location = geolocator.geocode(x)
    try:
        return location.longitude
    except Exception as e:
        return(0.0)

def get_lat(x):
    location = geolocator.geocode(x)
    try:
        return location.latitude
    except:
        return(0.0)

bekasi = load_pkl('.\pickle\det_data_bekasi.pkl')
depok =  load_pkl('.\pickle\det_data_depok.pkl')
tangsel =  load_pkl('.\pickle\det_data_tangsel.pkl')
tang =  load_pkl('.\pickle\det_data_tang.pkl')
timur = load_pkl('.\pickle\det_data_timur.pkl')
selatan = load_pkl('.\pickle\det_data_selatan.pkl')
utara = load_pkl('.\pickle\det_data_utara.pkl')
pusat = load_pkl('.\pickle\det_data_pusat.pkl')
barat = load_pkl('.\pickle\det_data_barat.pkl')

df_barat = pd.DataFrame.from_dict(barat)
df_timur =  pd.DataFrame.from_dict(timur)
df_selatan = pd.DataFrame.from_dict(selatan)
df_utara = pd.DataFrame.from_dict(utara)
df_pusat = pd.DataFrame.from_dict(pusat)
df_tang = pd.DataFrame.from_dict(tang)
df_tangsel = pd.DataFrame.from_dict(tangsel)
df_depok = pd.DataFrame.from_dict(depok)
df_bekasi = pd.DataFrame.from_dict(bekasi)

df_all = [df_barat, 
          df_timur,
          df_selatan,
          df_utara,
          df_pusat,
          df_tang,
          df_tangsel,
          df_depok,
          df_bekasi]

df = pd.concat(df_all, axis=0)

col_80 = (df.isna().sum()/len(df)).reset_index()
df.drop(labels=col_80[col_80[0] > 0.8]['index'].values, 
                  axis=1,
                  inplace=True)

df['price_juta'] = df['price'].apply(lambda x: float(x.lower().split(' ')[1]) if 'Rp' in x else 'NA')
df.drop(labels= df[df['price_juta'] == 'NA'].index,
            axis=0,
            inplace=True)

df.reset_index(drop=True, inplace=True)
df['installment_juta'] = df['installment'].apply(lambda x: float(x.split(' ')[1]))
df['kecamatan'] = df['address'].apply(lambda x: x.split(',')[0].strip())
df['provinsi'] = df['address'].apply(lambda x: x.split(',')[1].strip())
df['Longitude'] = df['address'].apply(lambda x: 0.0 if type(x) == type(None) else get_lon(x))
df['Latitude'] = df['address'].apply(lambda x: 0.0 if type(x) == type(None) else get_lat(x))

i_kec = df[df['Longitude'] == 0.0][['kecamatan','provinsi']].index

# manual edit for not found longitude latitiude
new_kec = ['Cibubur',
'Cibubur',
'Rawa Kalong',
'Pinang',
'Jelupang',
'Pancoran Mas',
'Pancoran Mas',
'Bekasi',
'Bekasi',
'Bekasi',
'Bekasi',
'Jatiasih',
'Jatiasih']

for e, index in enumerate(i_kec):
    df.at[index, 'kecamatan'] = new_kec[e]
    df.at[index, 'address'] = df.iloc[index]['kecamatan'] +', '+df.iloc[index]['provinsi']
    df.at[index, 'Longitude'] = get_lon(df.iloc[index]['address'])
    df.at[index, 'Latitude'] = get_lat(df.iloc[index]['address'])
    
df = df.assign(num_facilities = lambda x: x['facilities'].apply(lambda y: len(y.split(', '))))
df = df.assign(facilities = lambda x: x.facilities.apply(lambda f: f.lower()))
# wide_facilities = df.facilities.str.split(', ', expand=True).stack().reset_index(level = 1, drop = True)

df['outdoor_facilities'] = df['facilities'].apply(lambda x: 1 if re.compile(r'(taman|playground|jogging|lari|lapangan|renang)').search(x.lower()) else 0)
df['ac'] = df['facilities'].apply(lambda x: 1 if re.compile(r'ac').search(x.lower()) else 0)
df['security'] = df['facilities'].apply(lambda x: 1 if re.compile(r'(keamanan|cctv|security|one gate system)').search(x.lower()) else 0)
df['laundry'] = df['facilities'].apply(lambda x: 1 if re.compile(r'laundry|jemuran').search(x.lower()) else 0)
df['park'] = df['facilities'].apply(lambda x: 1 if re.compile(r'(carport|parkir)').search(x.lower()) else 0)

month_id = {'Januari': 'January', 
            'Februari': 'February', 
            'Maret': 'March', 
            'April': 'April', 
            'Mei': 'May', 
            'Juni': 'June', 
            'Juli': 'July', 
            'Agustus': 'August', 
            'September': 'September', 
            'Oktober': 'October', 
            'November': 'November', 
            'Desember': 'December'}

df = df.assign(published_date = lambda x: x['date'].apply(lambda y: y.replace('Tayang Sejak ','') ))
df = df.assign(day = lambda x: x.published_date.apply(lambda y: y.split(' ')[0]))
df = df.assign(month = lambda x: x.published_date.apply(lambda y: y.split(' ')[1].replace(',','')))
df = df.assign(year = lambda x: x.published_date.apply(lambda y: y.split(' ')[2]))
df['month'] = df['month'].map(month_id)

df['published_date'] = df['day'] + '-' + df['month'] + '-' + df['year']
df['published_date'] = df['published_date'].apply(lambda x: pd.to_datetime(x, format='%d-%B-%Y'))

df = df.assign(num_char_desc = lambda x: x['description'].apply(lambda c: len(c)))
df = df.assign(description = lambda x: x['description'].apply(lambda y: y.lower().strip()))

df['no_banjir'] = df['description'].apply(lambda x: 1 if re.compile(r'banjir').search(x.lower()) else 0)
df['transportation'] = df['description'].apply(lambda x: 1 if re.compile(r'(stasiun|krl|transjakarta|trans|lingko|busway|bus|bis|angkot|kereta)').search(x.lower()) else 0)

drop_cols = ['title', 'price', 'installment', 'date', 'address', 'rel_link', 'facilities', 'description', 'day', 'month', 'year']
df.drop(labels=drop_cols, axis=1, inplace=True)

df['L. Bangunan'] = df['L. Bangunan'].apply(lambda x: x if type(x) == float else float(x.split(' ')[0]))
df['L. Tanah'] = df['L. Tanah'].apply(lambda x: x if type(x) == float else float(x.split(' ')[0]))
df['price_juta'] = df['price_juta'].astype('float64')
df['L. Bangunan'] = df['L. Bangunan'].astype('float64')
df['L. Tanah'] = df['L. Tanah'].astype('float64')
df['K. Mandi'] = df['K. Mandi'].astype('float64')
df['K. Tidur'] = df['K. Tidur'].astype('float64')

df.to_csv('final_df.csv', index=False)