import json
from app import db
# from manage import db
from app.models import Item


class DataBasePipeline(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):
        print('*(**********databasePipeline', item, item['url'])
        for my_item in item['my_item']:
            item_entity = Item(url=item['url'], tag_id=my_item[0], data=my_item[1])
            db.session.add(item_entity)
        db.session.commit()
