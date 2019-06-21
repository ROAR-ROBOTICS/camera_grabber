#!/usr/bin/env python3  

import http.client
from html.parser import HTMLParser
import sys

link = '192.168.42.1'

conn = http.client.HTTPConnection(link)
conn.request("GET","/")
r = conn.getresponse()