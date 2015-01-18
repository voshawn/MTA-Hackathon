#! /usr/local/bin/python2.7 

import totalhandler
import xml.sax
 
parser = xml.sax.make_parser()
handler = totalhandler.TotalHandler()
parser.setContentHandler(handler)
parser.parse("http://advisory.mtanyct.info/LPUWebServices/CurrentLostProperty.aspx")