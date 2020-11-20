# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 12:01:37 2020

@author: sb_user
"""

import requests
import re

r = requests.get('https://www.tripadvisor.ru/Attraction_Review-g1439536-d2615844-Reviews-Khimki_Art_Gallery-Khimki_Moscow_Oblast_Central_Russia.html', verify=True)
print(r.status_code)
