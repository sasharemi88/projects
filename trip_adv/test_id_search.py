# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 12:01:37 2020

@author: sb_user
"""

from datetime import date as dt
import re
from datetime import timedelta as td
from dateutil.relativedelta import relativedelta as rd

def round_qtr (d):
    return(dt(d.year, 3*(d.month // 3)-2, 1))

def round_year (d):
    return(dt(d.year, 1, 1))
    
s = 'ЭйчЭм Хостел Москва '
s1 = re.sub('\"\"', '"', s)
s2 = re.sub('|^ | +$| $| ?\t', '', s1)

print(s2)