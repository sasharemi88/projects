from datetime import datetime

from tripadvisor.database import Session
from tripadvisor.database.models import LocationObject, get_first_day_of_quarter


class AllObjPipeline:
    def process_item(self, item, spider):
        return item


class SaveLocationPipeline:
    def __init__(self):
        self.session = Session()

    def process_item(self, item, spider):
        if item['object_id'] == '677301':
            print('ATTENTION')
        location = (
            self.session.query(LocationObject)
                .filter_by(object_id=item['object_id'])
                .one_or_none()
        )
        if location:
            location.name = item['name']
            location.address = item['address']
            location.category = item['category']
            location.subcategory = item['subcategory']
            location.subtype_cat = item['subtype']
            location.latitude = item['latitude']
            location.longitude = item['longitude']
            location.date_update = get_first_day_of_quarter(datetime.now())
            self.session.commit()
        else:
            location = LocationObject(
                object_id=item['object_id'],
                location_id=item['location_id'],
                name=item['name'],
                address=item['address'],
                category=item['category'],
                subcategory=item['subcategory'],
                subtype_cat=item['subtype'],
                latitude=item['latitude'],
                longitude=item['longitude']
            )
            self.session.add(location)
            self.session.commit()

        self.session.close()

        return item
