# -*- coding: utf-8 -*-
from urllib.parse import urljoin
import requests

def GetCount(id, api_key='cb0807044282aeab110f673516e689a5'):
    '''
    Функция получает кол-во объектов в категории.
    На вход:
        id категории (датасета - https://apidata.mos.ru/v1/datasets)
        api_key - ключ api сервиса, по умолчанию берется с аккаунта sasharemi88
    '''
    
    url = 'https://apidata.mos.ru/v1/datasets/' + str(id) + '/count?api_key=' + api_key
    r = requests.get(url)
    return (r.text)

print(GetCount(495))