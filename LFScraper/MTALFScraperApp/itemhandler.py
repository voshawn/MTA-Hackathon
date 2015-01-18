# item.py
from sqlalchemy import *
from sqlalchemy.orm import *
from time import gmtime, strftime
 
import xml.sax.handler
 
pg_db = create_engine('postgresql://mtasubway:123456@web432.webfaction.com:5432/mtalostfound')
 
metadata = MetaData(pg_db)
 
item_table = Table('items', metadata, autoload=True)
 
class Item(object):
    pass
 
mapper(Item, item_table)
 
class ItemHandler(xml.sax.handler.ContentHandler):
    def __init__(self):
        self.buffer = ""
        self.inField = 0
        self.session = create_session(bind=pg_db)
 
    def startElement(self, name, attributes):
        if name == "Category":
            self.category = attributes["Category"]
        elif name == "SubCategory":
            self.subcategory = attributes["SubCategory"]
            self.count = attributes["count"]

 
    def characters(self, data):
        if self.inField:
            self.buffer += data
 
    def endElement(self, name):
        if name == "SubCategory":
            self.session.begin()
            self.newitem = Item()
            self.newitem.category = self.category
            self.newitem.subcategory = self.subcategory
            self.newitem.count = self.count
            self.newitem.importtime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            self.session.add(self.newitem)
            self.session.commit()
        elif name == "Category":
            self.inField = 0
            self.category = self.buffer
        self.buffer = ""