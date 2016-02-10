# import json
# import os
# from app import db, create_app
# from manage import db, app
from app.models import Item, Result

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from manage import app


class DataBasePipeline(object):
    def __init__(self):
        uri = app.config['SQLALCHEMY_DATABASE_URI']
        print('SQLALCHEMY_DATABASE_URI = ', uri)
        self.engine = create_engine(uri)
        self.Session = sessionmaker(bind=self.engine)

    def process_item(self, item, spider):
        session = self.Session()
        print('*(**********databasePipeline', item, item['url'])
        result = Result(url=item['url'], task_id=item['task_id'])
        for my_item in item['my_item']:
            item_entity = Item(result=result, tag_id=my_item[0], data=my_item[1])
            session.add(item_entity)
        session.commit()
