#!/usr/bin/env python3  

import http.client
from html.parser import HTMLParser
import sys

# host = '192.168.42.1'
host = '192.168.42.1'
run_continuously = True
desired_extensions = ['jpg', 'jpeg'] # Capitalization ignored

class MyHTMLParser(HTMLParser):
    def __init__(self):
        self.rel_links = []
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            # print("Encountered a start tag:", tag)
            if attrs[0][0] == 'href':
                if attrs[0][1] == '../':
                    # Ignore link to previous site
                    return

            self.rel_links.append('/' + str(attrs[0][1]))

    def handle_endtag(self, tag):
        if tag == 'a':
            # print("Encountered an end tag :", tag)
            pass

    def handle_data(self, data):
        # print("Encountered some data  :", data)
        pass

def get_all_links(host, directory):
    conn = http.client.HTTPConnection(host)
    conn.request("GET", directory)
    r = conn.getresponse()
    print(r.status, r.reason)

    # Check HTTP response (Code 200 means OK)
    if r.status != 200:
        return None

    data = r.read()
    conn.close()

    parser = MyHTMLParser()
    parser.feed(str(data))
    return parser.rel_links

while(run_continuously):
    ## Get all directories from index site
    # directories = get_all_links(link, "/226E50HD/")
    directories = get_all_links(host, "/")

    if directories == None:
        # TODO: sleep for one second or something
        continue

    print("Found directories:")
    print(directories)
    print("")

    for d in directories:
        print("Fetching directory " + d)
        links = get_all_links(host, d)
        print(links)
        for l in links:
            # 

            # TODO: Does this need additional slashes?
            print("Downloading image " + host + d + l)
            # TODO: Download images to specified directory 

    # TODO: Sleep for some seconds

    exit()