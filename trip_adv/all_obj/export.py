from datetime import datetime
import csv
from datetime import date
import json
import re
from typing import Tuple, List

from tripadvisor.database import Session
from tripadvisor.database.models import LocationObject, get_first_day_of_quarter


def select_current_year() -> List[LocationObject]:
    """ Выборка записей за текущий год.

    Returns
    -------
    query : list
        Список экземпляров объекта LocationObject.

    """
    year = date.today().year
    session = Session()
    query = (
        session.query(LocationObject)
        .filter(LocationObject.date_create > datetime(year, 1, 1),
                LocationObject.latitude.isnot(None),
                # LocationObject.location_id == 2324025,
                LocationObject.address.isnot('')).all()
    )
    session.close()

    return query


def set_category(category: str, subcategory: str, subtypes: str) -> Tuple[str, str]:
    """ Получение категории и подкатегории.

    Parameters
    ----------
    category : str
        Категория.
    subcategory : str
        Подкатегория.
    subtypes : str
        Подтипы категории.

    Returns
    -------
        Tuple[category, subcategory]

    """
    matching = {
        ('attraction', ''): ['Достопримечательности', 'Развлечения'],
        ('attraction', 'Концерты и представления'): ['Отдых/развлечения/спорт', 'Развлечения'],
        ('attraction', 'Достопримечательности и культурные объекты'): ['Достопримечательности', 'Культурные объекты'],
        ('attraction', 'Природа и парки'): ['Достопримечательности', 'Парки'],
        ('attraction', 'Музеи'): ['Достопримечательности', 'Музеи'],
        ('attraction', 'Развлечения и игры'): ['Отдых/развлечения/спорт', 'Развлечения'],
        ('attraction', 'Еда и напитки'): ['Отдых/развлечения/спорт', 'Развлечения'],
        ('attraction', 'Активный отдых на открытом воздухе'): ['Отдых/развлечения/спорт', 'Развлечения'],
        ('attraction', 'Ресурсы для путешественников'): ['Туризм/транспорт', 'Турагенства'],
        ('attraction', 'Покупки'): ['Достопримечательности', 'Торговые центры'],
        ('attraction', 'Зоопарки и океанариумы'): ['Отдых/развлечения/спорт', 'Развлечения'],
        ('attraction', 'Туры'): ['Туризм/транспорт', 'Турагенства'],
        ('attraction', 'Ночная жизнь'): ['Отдых/развлечения/спорт', 'Развлечения'],
        ('attraction', 'Аквапарки и парки развлечений'): ['Отдых/развлечения/спорт', 'Развлечения'],
        ('attraction', 'Спа и оздоровление'): ['Красота и здоровье', 'Салоты красоты/массаж/SPA'],
        ('attraction', 'Мероприятия'): ['Отдых/развлечения/спорт', 'Прочие услуги'],
        ('attraction', 'Мастер-классы и семинары'): ['Отдых/развлечения/спорт', 'Прочие услуги'],
        ('attraction', 'Транспорт'): ['Туризм/транспорт', 'Общественный транспорт/Такси'],
        ('attraction', 'Другое'): ['Достопримечательности', 'Другое'],
        ('attraction', 'Казино и азартные игры'): ['Отдых/развлечения/спорт', 'Азартные игры'],
        ('attraction', 'Церкви и соборы'): ['Достопримечательности', 'Церкви и соборы'],
        ('hotel', 'Отель'): ['Туризм/транспорт', 'Отели'],
        ('hotel', 'B&B/мини-отель'): ['Туризм/транспорт', 'Отели'],
        ('hotel', 'Жилье особого типа'): ['Туризм/транспорт', 'Отели'],
        ('restaurant', 'Ресторан'): ['Кафе/бары/рестораны', 'Кафе/бары/рестораны'],
        ('restaurant', 'Кафе'): ['Кафе/бары/рестораны', 'Кафе/бары/рестораны'],
        ('restaurant', ''): ['Кафе/бары/рестораны', 'Кафе/бары/рестораны'],
        ('restaurant', 'Фаст-фуд'): ['Кафе/бары/рестораны', 'Фастфуд рестораны'],
    }
    try:
        tpl = matching[(category, subcategory)]
        if 'церкви и соборы' in subtypes.lower():
            return 'Достопримечательности', 'Церкви и соборы'
    except:
        print(f'No matches for {category, subcategory, subtypes}')
        return category, subcategory

    return tpl


def prepare(field):
    result = re.sub(r'\s+', ' ', field)
    result = result.strip()

    return result


def set_categories(records) -> List:

    result = []

    for record in records:
        record.category, record.subcategory = set_category(
            record.category, record.subcategory, record.subtype_cat
        )
        result.append(record)

    return result


def filter_records(records) -> List:

    result = []

    for record in records:
        if (record.subcategory != 'Отели') and (record.category != 'Кафе/бары/рестораны'):
            result.append(record)

    return result


def export_to_csv(file_path, query_records):
    file = open(file_path, 'w')
    writer = csv.writer(file, delimiter=';', skipinitialspace=True, strict=True)
    writer.writerow(['Широта', 'Долгота', 'Наименование', 'Адрес', 'Категория',
                     'Подкатегория', 'Дата', 'Тип даты'])
    for record in query_records:

        if get_first_day_of_quarter(datetime.now()) == record.date_update:
            row = [
                record.latitude,
                record.longitude,
                prepare(record.name),
                prepare(record.address),
                record.category,
                record.subcategory,
                record.date_update,
                'q'
            ]
            writer.writerow(row)

        row = [
            record.latitude,
            record.longitude,
            prepare(record.name),
            prepare(record.address),
            record.category,
            record.subcategory,
            record.date_update,
            'y'
        ]
        writer.writerow(row)

    file.close()


def export_to_json(file_path, query_records):

    json_data = {
        'type': 'FeatureCollection',
        'features': []
    }

    for record in query_records:

        feature = {
            'type': 'Feature',
            'properties': {
                'Название': record.name,
                'Адрес': record.address,
                'Категория': record.subcategory
            },
            'geometry': {
                'type': 'Point',
                'coordinates': [
                    round(float(record.longitude), 5),
                    round(float(record.latitude), 5)
                ]
            }
        }

        json_data['features'].append(feature)

    json.dump(json_data, open(file_path, 'w'), ensure_ascii=False)


if __name__ == '__main__':
    records = select_current_year()
    records = set_categories(records)
    # records = filter_records(records)
    # export_to_csv(f'report_{datetime.today().strftime("%d_%m_%Y")}.csv', records)
    export_to_json(f'report_{datetime.today().strftime("%d_%m_%Y")}.json', records)
    print()
