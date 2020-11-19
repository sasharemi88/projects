# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 17:04:39 2020

@author: Sasha
"""


import csv
import os
import re

#список файлов для обработки
files = ['Karelia.csv','Moscow.csv','NiNo.csv','Novgorod.csv','Samara.csv']



def rebuild(file):
    #словарь "категории трипадвизорва: категории МСС"
    cat_d = {('Отели',''): ('Средства размещения','Гостиницы и санатории'),
             ('Рестораны',''): ('Кафе/бары/рестораны','Кафе/бары/рестораны'),
             ('Достопримечательности','Музеи'): ('Развлечения','Музыка и искусство'),
             ('Достопримечательности','Еда и напитки'): ('Прочее','Прочее'),
             ('Достопримечательности','Достопримечательности и культурные объекты'): ('Развлечения','Музыка и искусство'),
             ('Достопримечательности','Природа и парки'): ('Развлечения','Зрелищные развлечения'),
             ('Достопримечательности', 'развлечения поблизости.'): ('Развлечения','Активные развлечения'),
             ('Достопримечательности','Покупки'): ('Непродовольственные магазины','Прочие товары'),
             ('Достопримечательности','Зоопарки и океанариумы'): ('Развлечения','Зрелищные развлечения'),
             ('Достопримечательности','Транспорт'): ('Транспорт','Общественный транспорт'),
             ('Достопримечательности','Ресурсы для путешественников'): ('Предоставление услуг','Турагенства'),
             ('Достопримечательности','Развлечения и игры'): ('Развлечения','Активные развлечения')
            }
    
    uniq = []
    
    file_in = os.path.join('all_obj', file)
    file_out = file   
    with open(file_in, 'r', encoding='utf8') as f:
        reader = csv.DictReader(f, delimiter=',')
        with open(file_out, 'w', newline='', encoding='utf8') as orign:
            fields = ['Широта', 'Долгота', 'Наименование', 'Адрес', 'Категория', 'Подкатегория', 'Дата парсинга']
            writer = csv.DictWriter(orign, fieldnames=fields, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar='',escapechar='\\')
            writer.writeheader()
            for line in reader:
                if line['с0_id'] not in uniq:
                    name = re.sub('^\"|\"$/g','', line['с6_name'])
                    adress = re.sub('^\"|\"$/g','', line['с7_adress'])
                    cat_key = (line['с3_category'], line['с4_subcategory'])
                    cat = cat_d[cat_key][0]
                    subcat = cat_d[cat_key][1]
                    writer.writerow({'Широта': line['с8_latitude'],
                                     'Долгота': line['с9_longitude'],
                                     'Наименование': re.sub('\"\"/g', '"', name),
                                     'Адрес':re.sub('\"\"/g', '"', adress) ,
                                     'Категория': cat,
                                     'Подкатегория': subcat,
                                     'Дата парсинга': line['с10_date']
                                    })
                    uniq.append(line['с0_id'])
    return print(file_in, ' - ', file_out)                

if __name__ == '__main__':
    for f in files:
        rebuild(f)