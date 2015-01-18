# bookhandler.py
from sqlalchemy import *
from sqlalchemy.orm import *
 
import xml.sax.handler
 
pg_db = create_engine('postgresql://mtasubway:123456@web432.webfaction.com:5432/mtalostfound')
 
metadata = MetaData(pg_db)
 
books_table = Table('books', metadata, autoload=True)
 
class Book(object):
    pass
 
mapper(Book, books_table)
 
class BookHandler(xml.sax.handler.ContentHandler):
    def __init__(self):
        self.buffer = ""
        self.inField = 0
        self.session = create_session(bind=pg_db)
 
    def startElement(self, name, attributes):
        if name == "book":
            self.isbn = attributes["isbn"]
        elif name == "title":
            self.inField = 1
        elif name == "author":
            self.inField = 1
 
    def characters(self, data):
        if self.inField:
            self.buffer += data
 
    def endElement(self, name):
        if name == "book":
            self.session.begin()
            self.newbook = Book()
            self.newbook.isbn = self.isbn
            self.newbook.title = self.title
            self.newbook.author = self.author
            self.session.add(self.newbook)
            self.session.commit()
        elif name == "title":
            self.inField = 0
            self.title = self.buffer
        elif name == "author":
            self.inField = 0
            self.author = self.buffer
        self.buffer = ""