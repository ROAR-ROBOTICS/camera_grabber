#!/usr/bin/env python3  

import time
import os
import http.client
from html.parser import HTMLParser
import urllib.request
import os.path


# Configuration
host = '192.168.42.1'
run_continuously = True
desired_extensions = ['jpg', 'jpeg']
download_dir = "/home/alessandro/Desktop/camera_grabber/"
verbose_output = True
connection_timeout = 10


class MyHTMLParser(HTMLParser):
    def __init__(self):
        self.rel_links = []
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            if attrs[0][0] == 'href':
                if attrs[0][1] == '../':
                    # Ignore link to previous site
                    return

            self.rel_links.append('/' + str(attrs[0][1]))

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        pass

def get_all_links(host, directory):
    try:
        conn = http.client.HTTPConnection(host, timeout=connection_timeout)
        conn.request("GET", directory)
        r = conn.getresponse()
    except OSError as e:
        print(e)
        return None

    # Check HTTP response (Code 200 means OK)
    if r.status != 200:
        print("HTTP error: ", r.status, r.reason)
        return None

    data = r.read()
    conn.close()

    parser = MyHTMLParser()
    parser.feed(str(data))
    return parser.rel_links

# Main loop
while(run_continuously):
    time.sleep(5)

    ## Get all directories from index site
    directories = get_all_links(host, "/")

    if directories == None:
        continue

    for d in directories:
        links = get_all_links(host, d)

        if links == None:
            continue

        for l in links:
            # Check if local file already exists
            fname = download_dir + d + l
            if os.path.isfile(fname):
                if verbose_output:
                    print("file " + fname + " already exists. Skipping download.")
                continue

            # Filter links by file extension
            filename, file_extension = os.path.splitext(fname)
            if file_extension[1:].lower() not in desired_extensions:
                if verbose_output:
                    print("Ignoring because of file extension: " + fname)
                continue

            file_url = "http://" + host + d + l
            print("Downloading file " + file_url + " to " + fname)

            # Download files to specified directory 
            try:
                with urllib.request.urlopen(file_url, timeout=connection_timeout) as response:
                    # Create target download directory if necessary
                    if not os.path.exists(download_dir + d):
                        os.makedirs(download_dir + d)

                    downloaded_data = response.read()
                    F = open(fname, 'w+b')

                    F.write(downloaded_data)
                    F.close()
            except:
                continue