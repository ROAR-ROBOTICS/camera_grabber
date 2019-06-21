#!/usr/bin/env python3  

import http.client
from html.parser import HTMLParser
import sys
import urllib.request

# host = '192.168.42.1'
host = '192.168.42.1'
run_continuously = True
desired_extensions = ['jpg', 'jpeg'] # Capitalization ignored
download_dir = "/home/alessandro/Desktop/camera_grabber/"


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
            # Filter links
            # TODO: Check file extension against our whitelist


            file_url = "http://" + host + d + l

            # TODO: Does this need additional slashes?
            print("Downloading file " + file_url)

            # TODO: Download images to specified directory 
            with urllib.request.urlopen(file_url) as response:
                downloaded_data = response.read()
                F = open("download", 'w+b')

                 # TODO: Is this the right way to write binary data?
                 # ... it does not work like this...
                F.write(downloaded_data)
                F.close()
                exit()



    # TODO: Sleep for some seconds

    exit()