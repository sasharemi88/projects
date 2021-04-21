import json

import scrapy
import datetime
import re


HEADERS = {'X-TripAdvisor-API-Key': 'ce957ab2-0385-40f2-a32d-ed80296ff67f',
           'X-TripAdvisor-UUID': '9bd844a6-231f-437b-b752-e5a1acbfee09'}


class TripSpider(scrapy.Spider):
    name = 'tripadvisor'

    def start_requests(self):
        locations = [
            2324019,  # Алтайский край
            2323906,  # Амурская область
            2323924,  # Архангельская область
            2323928,  # Астраханская область
            2323940,  # Белгородская область
            2323942,  # Брянская область
            2323965,  # Владимирская область
            2323936,  # Волгоградская область
            2324029,  # Вологодская область
            2323967,  # Воронежская область
            2324042,  # Еврейская автономная область
            2324020,  # Забайкальский край
            2323944,  # Ивановская область
            2323984,  # Иркутская область
            2324087,  # Кабардино-Балкарская Республика
            2324022,  # Калининградская область
            2323946,  # Калужская область
            2324090,  # Карачаево-Черкесская Республика
            2323989,  # Кемеровская область
            2324048,  # Кировская область
            2323947,  # Костромская область
            2323938,  # Краснодарский край
            2324021,  # Красноярский край
            2323974,  # Курганская область
            2323948,  # Курская область
            2324023,  # Ленинградская область
            2323950,  # Липецкая область
            2324034,  # Магаданская область
            2323955,  # Московская область *
            298484,   # Москва *
            2324024,  # Мурманская область
            2324032,  # Ненецкий автономный округ
            2324049,  # Нижегородская область
            2324025,  # Новгородская область
            2323995,  # Новосибирская область
            2324008,  # Омская область
            1087652,  # Оренбургская область
            2323957,  # Орловская область
            2324053,  # Пензенская область
            2324084,  # Пермский край
            2324040,  # Приморский край
            2324027,  # Псковская область
            2323937,  # Республика Адыгея
            1833666,  # Республика Алтай
            298517,   # Республика Башкортостан
            2324015,  # Республика Бурятия
            1536793,  # Республика Дагестан
            679470,   # Республика Ингушетия
            1207891,  # Республика Калмыкия
            298504,  # Республика Карелия
            2324091,  # Республика Коми
            313972,   # Крымнаш *
            2324066,  # Республика Марий Эл
            2324071,  # Республика Мордовия
            2324038,  # Республика Саха (Якутия)
            1600259,  # Республика Северная Осетия - Алания
            298519,   # Республика Татарстан
            2324016,  # Республика Тыва
            2324017,  # Республика Хакасия
            2323930,  # Ростовская область
            2323959,  # Рязанская область
            298507,   # Санкт-Петербург *
            2324059,  # Саратовская область
            2324035,  # Сахалинская область
            2324055,  # Самарская область
            2323977,  # Свердловская область
            295387,   # Севастополь
            2323960,  # Смоленская область
            2324094,  # Ставропольский край
            2323961,  # Тамбовская область
            2323963,  # Тверская область
            2324012,  # Томская область
            2323964,  # Тульская область
            2323978,  # Тюменская область
            2324078,  # Удмуртская республика
            2324064,  # Ульяновская область
            2324041,  # Хабаровский край
            2323979,  # Ханты-Мансийский АО
            2323973,  # Челябинская область
            494956,   # Чеченская республика
            2324083,  # Чувашская республика
            1540820,  # Чукотский АО
            2323982,  # Ямало-Ненецкий АО
            2323968,  # Ярославская область
        ]
        for location_id in locations:
            HEADERS.update({'Content-Type': 'application/x-www-form-urlencoded'})
            yield scrapy.Request(
                url='https://api.tripadvisor.com/api/internal/1.19/meta_hac/{}'.format(location_id),
                method='POST',
                headers=HEADERS,
                body='currency=RUB&lang=ru&limit=50&lod=extended',
                callback=self.parse_objects,
                meta={'location_id': location_id})

            HEADERS.update({'Content-Type': 'application/json'})
            yield scrapy.Request(
                url='https://api.tripadvisor.com/api/internal/1.14/location/{}/restaurants?limit=50&offset=0&lang=ru'.format(location_id),
                headers=HEADERS,
                callback=self.parse_objects,
                meta={'location_id': location_id})

            yield scrapy.Request(
                url='https://api.tripadvisor.com/api/internal/1.14/location/{}/attractions?limit=50&offset=0&lang=ru'.format(location_id),
                headers=HEADERS,
                callback=self.parse_objects,
                meta={'location_id': location_id})

    def parse_objects(self, response):
        result = json.loads(response.text)
        location_id = response.meta.get('location_id')
        print(location_id)
        objects = result['data']

        for obj in objects:
            category = obj.get('category').get('key')
            subcategory = obj.get('subcategory')
            if subcategory:
                subcategory = re.sub(r'\xa0', ' ', subcategory[0]['name'])
            else:
                subcategory = ''
            subtypes = obj.get('subtype')
            if subtypes:
                subtypes = ','.join(
                    re.sub(r'\xa0', ' ', x['name']) for x in subtypes
                )
            else:
                subtypes = ''

            # category, subcategory = replace_categories(category, subcategory, subtypes)

            # for d_tuple in split_dates():
            #     yield {
            #         'Широта': obj.get('latitude'),
            #         'Долгота': obj.get('longitude'),
            #         'Наименование': obj.get('name'),
            #         'Адрес': obj.get('address'),
            #         'Категория': category,
            #         'Подкатегория': subcategory,
            #         'Подтипы категории': subtypes,
            #         'Дата': d_tuple[0],
            #         'Тип даты': d_tuple[1],
            #         'location_id': location_id
            #     }

            yield {
                'object_id': obj.get('location_id'),
                'location_id': location_id,
                'name': obj.get('name'),
                'category': category,
                'subcategory': subcategory,
                'subtype': subtypes,
                'address': obj.get('address'),
                'latitude': obj.get('latitude'),
                'longitude': obj.get('longitude'),
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
                                      callback=self.parse_objects,
                                      meta={'location_id': location_id})
            else:
                yield response.follow(url=next_page,
                                      headers=response.request.headers,
                                      dont_filter=True,
                                      callback=self.parse_objects,
                                      meta={'location_id': location_id})


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
