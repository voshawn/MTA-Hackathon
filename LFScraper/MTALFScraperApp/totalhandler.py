# item.py
from sqlalchemy import *
from sqlalchemy.orm import *
from time import gmtime, strftime
 
import xml.sax.handler
 
pg_db = create_engine('postgresql://mtasubway:123456@web432.webfaction.com:5432/mtalostfound')
 
metadata = MetaData(pg_db)
 
totals_table = Table('totals', metadata, autoload=True)
 
class Total(object):
    pass
 
mapper(Total, totals_table)
 
class TotalHandler(xml.sax.handler.ContentHandler):
    def __init__(self):
        self.buffer = ""
        self.inField = 0
        self.session = create_session(bind=pg_db)
 
    def startElement(self, name, attributes):
        if name == "NumberOfLostArticles":
            self.inField = 1
        elif name =="NumberOfItemsclaimed":
            self.inField = 1

 
    def characters(self, data):
        if self.inField:
            self.buffer += data
 
    def endElement(self, name):
        if name == "NumberOfItemsclaimed":
            self.session.begin()
            self.newtotal = Total()
            self.newtotal.lostcount = self.NumberOfLostArticles
            self.newtotal.claimcount = self.buffer
            self.newtotal.importtime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            self.session.add(self.newtotal)
            self.session.commit()
        elif name == "NumberOfLostArticles":
            self.inField = 0
            self.NumberOfLostArticles = self.buffer
            self.buffer = ""