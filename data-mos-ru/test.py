from urllib.parse import urljoin
import requests
import json
from func import GetCount
import csv

url = 'https://apidata.mos.ru/v1/datasets'

param = {'?api_key=': 'cb0807044282aeab110f673516e689a5',
         #'&$top=': 10,
         '&$skip=': 0         
        }
s=''
for i in param.items():    
    s = s + i[0]+str(i[1])

url = urljoin(url, s)
r = requests.get(url)
j = json.loads(r.text)


with open ('mosdata.csv', 'w', newline='', encoding='utf8') as file:
    fields = ['id', 'cat_name', 'count']
    writer = csv.DictWriter(file, fieldnames=fields, delimiter=';')
    writer.writeheader()
    for i in j:
        writer.writerow({'id':i['Id'],
                         'cat_name':i['Caption'],
                         'count': GetCount(i['Id'])})
        print(i['Id'])
        print(i['Caption'])
        print(GetCount(i['Id']))
        print('----')
    
#%%
url2 = 'https://apidata.mos.ru/v1/datasets/495/rows'   
param2 = {'?api_key=': 'cb0807044282aeab110f673516e689a5'
           }
s2=''
for i in param2.items():    
    s2 = s2 + i[0]+str(i[1])
url2 = urljoin(url2, s2)
r2 = requests.get(url2)
j2 = json.loads(r2.text)

for i in j2:
    print(i['Cells']['CommonName']) 
    print(i['Cells']['geoData']["type"])
    print(i['Cells']['geoData']['coordinates'])
    print('____')

#%%
url3 = 'https://apidata.mos.ru/v1/datasets/495/count?api_key=cb0807044282aeab110f673516e689a5'   
r3 = requests.get(url3)
print (r3.text)