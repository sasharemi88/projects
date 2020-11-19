import requests
import re
from datetime import datetime

print(datetime.date(datetime.today()))

#для достопримечательостей и ресторанов
r = requests.get('https://www.tripadvisor.ru/Attraction_Review-g298515-d3445884-Reviews-Nizhny_Novgorod_Cableroads-Nizhny_Novgorod_Nizhny_Novgorod_Oblast_Volga_District.html')
lat_pat = re.compile('"latitude":"\d+.\d+"')
lat = lat_pat.search(r.text).group(0).split(':')[1].replace('"', '').replace(' ', '')
lon_pat = re.compile('"longitude":"\d+.\d+"')
lon = lon_pat.search(r.text).group(0).split(':')[1].replace('"', '').replace(' ', '')
print(lat, ';', sep='')
print(lon)

#для отелей
r2 = requests.get('https://www.tripadvisor.ru/Hotel_Review-g298515-d12551166-Reviews-Sheraton_Nizhny_Novgorod_Kremlin-Nizhny_Novgorod_Nizhny_Novgorod_Oblast_Volga_Distric.html')
coor_pat = re.compile('"coords":"\d+.\d+,\d+.\d+"')
coor = coor_pat.search(r2.text).group(0).split(':')[1].replace('"', '')
lat2 = coor.split(',')[0]
lon2 = coor.split(',')[1]
print(lat2, ', ', lon2)
