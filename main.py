#!/usr/bin/env python3  

import http.client
from html.parser import HTMLParser
import sys

# link = '192.168.42.1'
link = '192.168.42.1'

class MyHTMLParser(HTMLParser):
    def __init__(self):
        # self.parsing_link = False
        self.rel_links = []
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            print("Encountered a start tag:", tag)
            # self.parsing_link = True
            if attrs[0][0] == 'href':
                if attrs[0][1] == '../':
                    return

                # full_link = link + )
                # print(full_link)
            self.rel_links.append('/' + str(attrs[0][1]))

    def handle_endtag(self, tag):
        # if tag == 'a':
        print("Encountered an end tag :", tag)
        #     self.parsing_link = False

    def handle_data(self, data):
        # if self.parsing_link:
        print("Encountered some data  :", data)

def get_all_links(host, directory):
    conn = http.client.HTTPConnection(link)
    conn.request("GET", directory)
    r = conn.getresponse()
    print(r.status, r.reason)

    # Check HTTP response (Code 200 means OK)
    if r.status != 200:
        # TODO: Handle gracefully
        print("Error connecting to camera")
        exit()

    data = r.read()
    conn.close()

    parser = MyHTMLParser()
    parser.feed(data)
    return parser.rel_links

## Get all directories from index site
# directories = get_all_links(link, "/226E50HD/")
directories = get_all_links(link, "/")
print("Directories:")
print(directories)

for d in directories:
    print("Fetching directory " + d)
    links = get_all_links(d)
    print(links)



    # conn = http.client.HTTPConnection(d)
    # conn.request("GET","/")
    # r1 = conn.getresponse()
    # print(r1.status, r1.reason)

    # if r1.status != 200:
    #     print("Error connecting to camera")
    #     exit()

    # data = r1.read()
    # conn.close()

    # parser2 = MyHTMLParser()
    # parser.feed(data)

    # print("Files: ")
    # print(parser.links)