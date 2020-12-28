import json

import scrapy
import datetime
import re


HEADERS = {'X-TripAdvisor-API-Key': 'ce957ab2-0385-40f2-a32d-ed80296ff67f',
           'X-TripAdvisor-UUID': '9bd844a6-231f-437b-b752-e5a1acbfee09'}


class AllObjectSpider(scrapy.Spider):
    name = 'tripadvisor'

    def start_requests(self):
        locations = [
            # 2324012,  # Томская область
            # 2324094,  # Ставропольский край
            # 2323928,  # Астраханская область
            # 2323978,  # Тюменская область
            # 2324091,  # Республика Коми
            # 2324029,  # Вологодская область
            # 2323947,  # Костромская область
            # 2324034,  # Магаданская область
            # 1087652,  # Оренбургская область
            # 2323968,  # Ярославская область
            # 2323965,  # Владимирская область
            # 2323984,  # Иркутская область
            2324040,  # Приморский край
        ]
        for location_id in locations:
            HEADERS.update({'Content-Type': 'application/x-www-form-urlencoded'})
            yield scrapy.Request(
                url='https://api.tripadvisor.com/api/internal/1.19/meta_hac/{}'.format(location_id),
                method='POST',
                headers=HEADERS,
                body='currency=RUB&lang=ru&limit=50&lod=extended', callback=self.parse_objects)

            HEADERS.update({'Content-Type': 'application/json'})
            yield scrapy.Request(
                url='https://api.tripadvisor.com/api/internal/1.14/location/{}/restaurants?limit=50&offset=0&lang=ru'.format(location_id),
                headers=HEADERS,
                callback=self.parse_objects)

            yield scrapy.Request(
                url='https://api.tripadvisor.com/api/internal/1.14/location/{}/attractions?limit=50&offset=0&lang=ru'.format(location_id),
                headers=HEADERS,
                callback=self.parse_objects)

    def parse_objects(self, response):
        result = json.loads(response.text)
        objects = result['data']

        for obj in objects:
            category = obj.get('category').get('key')
            subcategory = obj.get('subcategory')
            if subcategory:
                subcategory = re.sub(r'\xa0', ' ', subcategory[0]['name'])
            subtypes = obj.get('subtype')
            if subtypes:
                subtypes = ','.join(x['name'] for x in subtypes)

            # category, subcategory = replace_categories(category, subcategory, subtypes)

            for d_tuple in split_dates():
                yield {
                    'Широта': obj.get('latitude'),
                    'Долгота': obj.get('longitude'),
                    'Наименование': obj.get('name'),
                    'Адрес': obj.get('address'),
                    'Категория': category,
                    'Подкатегория': subcategory,
                    'Подтипы категории': subtypes,
                    'Дата': d_tuple[0],
                    'Тип даты': d_tuple[1]
                }

        next_page = result['paging'].get('next')
        if next_page:
            if objects[0]['category']['key'] == 'hotel':
                body = next_page.split('?')[1]
                yield response.follow(url=response.url,
                                      method='POST',
                                      headers=response.request.headers,
                                      body=body,
                                      dont_filter=True,
                                      callback=self.parse_objects)
            else:
                yield response.follow(url=next_page,
                                      headers=response.request.headers,
                                      dont_filter=True,
                                      callback=self.parse_objects)


def replace_categories(category, subcategory, subtypes):
    return category, subcategory, subtypes

    # Пока сбор с оригинальными категоирями, после согласования всех соответствий
    # категорий/подкатегорий можно раскомментировать и поправить код ниже.

    # cat_d = {'Музеи': ('Достопримечательности', 'Музеи'),
    #          'Еда и напитки': ('Отдых/развлечения/спорт', 'Развлечения'),
    #          'Достопримечательности и культурные объекты': ('Достопримечательности', 'Культурные объекты'),
    #          'Природа и парки': ('Достопримечательности', 'Парки'),
    #          'Покупки': ('Достопримечательности', 'Торговые центры'),
    #          'Зоопарки и океанариумы': ('Отдых/развлечения/спорт', 'Развлечения'),
    #          'Транспорт': ('Туризм/транспорт', 'Общественный транспорт/Такси'),
    #          'Ресурсы для путешественников': ('Туризм/транспорт', 'Турагенства'),
    #          'Развлечения и игры': ('Отдых/развлечения/спорт', 'Развлечения'),
    #          'Аквапарки и парки развлечений': ('Отдых/развлечения/спорт', 'Развлечения'),
    #          'Концерты и представления': ('Отдых/развлечения/спорт', 'Развлечения'),
    #          'Казино и азартные игры': ('Отдых/развлечения/спорт', 'Азартные игры'),
    #          'Активный отдых на открытом воздухе': ('Отдых/развлечения/спорт', 'Развлечения')
    #          }
    #
    # if category == 'hotel':
    #     return 'Туризм/транспорт', 'Отели'
    # if category == 'restaurant':
    #     return 'Кафе/бары/рестораны', 'Кафе/бары/рестораны'
    # if category == 'attraction':
    #     if subtypes:
    #         subtypes = [st['name'].lower() for st in subtypes]
    #         if 'церкви и соборы' in subtypes:
    #             return 'Достопримечательности', 'Церкви и соборы'
    #
    #     try:
    #         return cat_d.get(subcategory)
    #     except:
    #         print('{} - НЕТ В СЛОВАРЕ СОПОСТАВЛЕНИЯ!')
    #         return category, subcategory
    #
    # return category, subcategory


def split_dates(delta=3):
    """ Разделение дат на кварталы и годы.

    Parameters
    ----------
    delta : int
        На сколько лет назад сделать расчет.
    Returns
    -------

    """
    dates_list = []
    today = datetime.date.today()

    for year in range(delta):
        dates_list.append((datetime.date(today.year - year, 1, 1), 'y'))
        for month in [1, 4, 7, 10]:
            dates_list.append((datetime.date(today.year - year, month, 1), 'q'))

    return dates_list
