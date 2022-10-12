from matplotlib.artist import get
from scrapping_libs import load_pkl, dump_pkl, get_detail_data

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0'
}

# get detail data
barat = load_pkl('.\pickle\link_date_rumah123_jakarta-barat_minmaxprice.pkl')
pusat = load_pkl('.\pickle\link_date_rumah123_jakarta-pusat_minmaxprice.pkl')
utara = load_pkl('.\pickle\link_date_rumah123_jakarta-utara_minmaxprice.pkl')
selatan = load_pkl('.\pickle\link_date_rumah123_jakarta-selatan_minmaxprice.pkl')
timur = load_pkl('.\pickle\link_date_rumah123_jakarta-timur_minmaxprice.pkl')
tang  = load_pkl('.\pickle\link_date_rumah123_tangerang_minmaxprice.pkl')
tangsel = load_pkl('.\pickle\link_date_rumah123_tangerang-selatan_minmaxprice.pkl')
depok = load_pkl('.\pickle\link_date_rumah123_depok_minmaxprice.pkl')
bekasi = load_pkl('.\pickle\link_date_rumah123_bekasi_minmaxprice.pkl')

# barat
det_data = []
for x, reldate in enumerate(barat):
    det_data_crrnt = get_detail_data(reldate, header)
    det_data.append(det_data_crrnt)   
    if x % 10 == 0:
        dump_pkl(det_data, f'.\pickle\det_data_barat_temp.pkl')
        print(f'data barat saved = {x}')  
dump_pkl(det_data, f'.\pickle\det_data_barat.pkl')

# pusat
det_data = []
for x, reldate in enumerate(pusat):
    det_data_crrnt = get_detail_data(reldate, header)
    det_data.append(det_data_crrnt)   
    if x % 10 == 0:
        dump_pkl(det_data, f'.\pickle\det_data_pusat_temp.pkl')
        print(f'data pusat saved = {x}')  
dump_pkl(det_data, f'.\pickle\det_data_pusat.pkl')

# # utara
det_data = []
for x, reldate in enumerate(utara):
    det_data_crrnt = get_detail_data(reldate, header)
    det_data.append(det_data_crrnt)   
    if x % 10 == 0:
        dump_pkl(det_data, f'.\pickle\det_data_utara_temp.pkl')
        print(f'data utara saved = {x}')  
dump_pkl(det_data, f'.\pickle\det_data_utara.pkl')

# # selatan
det_data = []
for x, reldate in enumerate(selatan):
    det_data_crrnt = get_detail_data(reldate, header)
    det_data.append(det_data_crrnt)   
    if x % 10 == 0:
        dump_pkl(det_data, f'.\pickle\det_data_selatan_temp.pkl')
        print(f'data selatan saved = {x}')  
dump_pkl(det_data, f'.\pickle\det_data_selatan.pkl')

# timur
det_data = []
for x, reldate in enumerate(timur):
    det_data_crrnt = get_detail_data(reldate, header)
    det_data.append(det_data_crrnt)   
    if x % 10 == 0:
        dump_pkl(det_data, f'.\pickle\det_data_timur_temp.pkl')
        print(f'data timur saved = {x}')  
dump_pkl(det_data, f'.\pickle\det_data_timur.pkl')

# tang
det_data = []
for x, reldate in enumerate(tang):
    det_data_crrnt = get_detail_data(reldate, header)
    det_data.append(det_data_crrnt)   
    if x % 10 == 0:
        dump_pkl(det_data, f'.\pickle\det_data_tang_temp.pkl')
        print(f'data tang saved = {x}')  
dump_pkl(det_data, f'.\pickle\det_data_tang.pkl')

# tangsel
det_data = []
for x, reldate in enumerate(tangsel):
    det_data_crrnt = get_detail_data(reldate, header)
    det_data.append(det_data_crrnt)   
    if x % 10 == 0:
        dump_pkl(det_data, f'.\pickle\det_data_tangsel_temp.pkl')
        print(f'data tangsel saved = {x}')  
dump_pkl(det_data, f'.\pickle\det_data_tangsel.pkl')

# depok
det_data = []
for x, reldate in enumerate(depok):
    det_data_crrnt = get_detail_data(reldate, header)
    det_data.append(det_data_crrnt)   
    if x % 10 == 0:
        dump_pkl(det_data, f'.\pickle\det_data_depok_temp.pkl')
        print(f'data depok saved = {x}')  
dump_pkl(det_data, f'.\pickle\det_data_depok.pkl')

# bekasi
det_data = []
for x, reldate in enumerate(bekasi):
    det_data_crrnt = get_detail_data(reldate, header)
    det_data.append(det_data_crrnt)   
    if x % 10 == 0:
        dump_pkl(det_data, f'.\pickle\det_data_bekasi_temp.pkl')
        print(f'data bekasi saved = {x}')  
dump_pkl(det_data, f'.\pickle\det_data_bekasi.pkl')