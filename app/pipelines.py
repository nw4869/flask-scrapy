import json
from app import db
from app.models import Item


class JsonWriterPipeline(object):
    def __init__(self):
        self.file = open('items.jl', 'wb')

    def process_item(self, item, spider):
        print('*(**********JsonWriter', item)
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item


class DataBasePipeline(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):
        # print('*(**********databasePipeline', item, item['url'])
        for my_item in item['my_item']:
            item_entity = Item(url=item['url'], tag_id=my_item[0], data=my_item[1])
            db.session.add(item_entity)
        db.session.commit()
