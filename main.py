#!/usr/bin/env python3  

import time
import os
import http.client
from html.parser import HTMLParser
# import sys
import urllib.request
import os.path

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

    # Check HTTP response (Code 200 means OK)
    if r.status != 200:
        print("HTTP error: ", r.status, r.reason)
        return None

    data = r.read()
    conn.close()

    parser = MyHTMLParser()
    parser.feed(str(data))
    return parser.rel_links

while(run_continuously):
    ## Get all directories from index site
    directories = get_all_links(host, "/")

    if directories == None:
        # TODO: sleep for one second or something
        continue

    # print("Found directories:")
    # print(directories)
    # print("")

    for d in directories:
        # print("Fetching directory " + d)
        links = get_all_links(host, d)
        # print(links)
        for l in links:
            # Check if file already exists
            fname = download_dir + d + l
            if os.path.isfile(fname):
                print("file " + fname + " already exists. Skipping download.")
                continue


            # Filter links
            # TODO: Check file extension against our whitelist
            # if "mp4" in l: # Skip mp4 for testing only
            #     print("Skipping " + l)
            #     continue
            filename, file_extension = os.path.splitext(fname)
            if file_extension[1:] not in desired_extensions:
                print("Ignoring because of file extension: " + fname)
                continue


            file_url = "http://" + host + d + l

            print("Downloading file " + file_url + " to " + fname)

            # TODO: Download images to specified directory 
            with urllib.request.urlopen(file_url) as response:
                # Create target download directory if necessary
                if not os.path.exists(download_dir + d):
                    os.makedirs(download_dir + d)

                downloaded_data = response.read()
                F = open(fname, 'w+b')

                 # TODO: Is this the right way to write binary data?
                 # ... it does not work like this...
                F.write(downloaded_data)
                F.close()
                # exit()
                # break



    # TODO: Sleep for some seconds
    print("Done - Sleeping for 5 seconds")
    time.sleep(5)
