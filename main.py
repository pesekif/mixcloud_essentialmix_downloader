#!/usr/bin/env python

import requests
import re
import schedule
import os
from selenium import webdriver

import sys
import time
import threading
from pathlib import Path


base_url = 'https://www.mixcloud.com/essentialmixcollection/'

file_dir = '/media/dave/bigdisk/emixes'
#file_dir = '/media/dave/bigdisk/emixes_tmp'

#file_dir = '/tmp'

def downloadPage(year, playlist_name,slimit):
    purl = setupPlaylistURL(year,playlist_name)
    htmlSource = getHTMLSource(purl,slimit)
    downloadMixes(htmlSource)

def setupPlaylistURL(year,playlist_name):
    return_url = 'https://www.mixcloud.com/essentialmixcollection/'
    if(year is None):
        return return_url
    if(playlist_name is '' and year):
        playlist_name = year
    return "{}playlists/{}/".format(return_url,playlist_name)

def getHTMLSource(url,slimit):
    print("Browser setup : {}".format(url))
    sys.path.append('/usr/lib/chromium-browser/')
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    options.add_argument("--headless")
    options.binary_location = "/usr/bin/chromium-browser"

    driver = webdriver.Chrome('./chromedriver/chromedriver', chrome_options=options)
    driver.get(url)

    for i in range(0, slimit, 1):
        print("Scroll")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)
        htmltext = driver.page_source
        print(len(htmltext))

    return htmltext

def createYearDir(year):
    # Create file directory
    year_dir = "{}/{}".format(file_dir, year)
    try:
        os.mkdir(year_dir)
    except:
        pass
    return year_dir


def fileExist(file):
    if (Path(file).exists()):
        return True
    return False

def extractMixes(htmltext):
    matches = re.findall('/(essentialmixcollection/([21][^\/]+))/"', htmltext)
    # print("Matches")
    filtered = {match: '' for match in matches}
    print("\nFULL FILTERED : {}".format(filtered))
    print("Number of mixes to DL  {}".format(len(filtered.keys())))
    #time.sleep(5)
    #sys.exit()
    return filtered

def downloadMixes(htmltext):

    #eurl = "{}/{}-{}".format(base_url, 'playlists/essential-mix', year)
    # print(eurl)
    #response = requests.get(eurl)
    filtered = extractMixes(htmltext)
    for match in filtered.keys():
        year = re.match('^\d{4}', match[1])
        print(year)
        if(year):
            year = year.group(0)
        print(year)
        #sys.exit()
        year_dir = createYearDir(year)
        # href="/essentialmixcollection/20180203-essential-mix-lone/"
        # https://www.mixcloud.com/essentialmixcollection/20180217-essential-mix-len-faki/


        # print("EMIX MATCH : {}".format(match))
        mix_url = "{}{}/".format(base_url, match[1])
        # print(mix_url)
        # http: // download.mixcloud - downloader.com / d / mixcloud / essentialmixcollection / 20180310 - essential - mix - peggy - gou
        mcd_url = "{}/{}/".format('http://download.mixcloud-downloader.com/d/mixcloud', match[0])
        emix_file = "{}/{}.mp4".format(year_dir, match[1])
        print("Downloading from : {}".format(mcd_url))
        print("Destination file : {}".format(emix_file))
        if (fileExist(emix_file)):
            print("Skipping {} - reason - already exists".format(emix_file))
            continue

        temp_file = "{}.tmp".format(emix_file)

        r = requests.get(mcd_url, stream=True, verify=False)


        with open(temp_file, 'wb') as MP4:
            for chunk in r.iter_content(chunk_size=1024):
                # writing one chunk at a time to pdf file
                if chunk:
                    MP4.write(chunk)
        
        os.rename(temp_file, emix_file)


def main():
    print("hello")
    years = [ y for y in range(1993,2020,1) ]
    years_hash = { y:'essential-mix-'+str(y) for y in years}
    years_hash[1993] = ''
    print(years_hash)
    base_url = ''

    downloadPage(None, None,90)
    sys.exit()

    for year in sorted(years_hash.keys()):
        print(year)
        playlist=years_hash[year]
        downloadPage(year, playlist,5)
        #job_thread = threading.Thread(target=downloadYear, kwargs={'year' : year, 'playlist_name' : playlist})
        #job_thread.start()
        time.sleep(5)
    print("Done")



if __name__ == '__main__':

    main()