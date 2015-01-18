#! /usr/local/bin/python2.7 

import itemhandler
import xml.sax
 
parser = xml.sax.make_parser()
handler = itemhandler.ItemHandler()
parser.setContentHandler(handler)
parser.parse("http://advisory.mtanyct.info/LPUWebServices/CurrentLostProperty.aspx")

parser = xml.sax.make_parser()
handler = totalhandler.TotalHandler()
parser.setContentHandler(handler)
parser.parse("http://advisory.mtanyct.info/LPUWebServices/CurrentLostProperty.aspx")