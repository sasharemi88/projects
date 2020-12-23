# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 12:33:19 2020

@author: sb_user
"""
import re

s = 'https://www.tripadvisor.ru/Attractions-g2323944-Activities-oa120-Ivanovo_Oblast_Central_Russia.html'
p1 = s.split('-Activities')[0]
p2 = re.sub('-oa\d+', '', s.split('-Activities')[1])
s1 = p1 + '-Activities-oa' + '60' + p2

print(p2)
print('----')
print(s1)
