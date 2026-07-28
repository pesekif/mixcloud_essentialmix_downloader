#!/usr/bin/env python

import requests
import re
import os
from selenium import webdriver

import sys
import time
import threading
from pathlib import Path

base_url = 'https://www.mixcloud.com/essentialmixcollection/'
file_dir = '/media/dave/bigdisk/emixes'

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
    sys.path.append('/usr/local/bin/')
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    options.add_argument("--headless")
    options.binary_location = "/usr/local/bin/chromedriver"

    driver = webdriver.Chrome(options = options)
    
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
    '''
    Simple routine to check if a file exists or not to prevent stamping over an 
    existing downloaded file
    '''
    if (Path(file).exists()):
        return True
    return False

def extractMixes(htmltext: str):
    '''
    Extract the mix name from the URLS found within the htmlpage
    
    Args:
        htmltext: str, holding a Mixcloud htmltext page for analysis
    
    Returns:
        filtered: Dict, representing all the mixes found in the html text
    ''' 
    matches = re.findall('/(essentialmixcollection/([21][^\/]+))/"', htmltext)
    filtered = {match: '' for match in matches}
    print("\nFULL FILTERED : {}".format(filtered))
    print("Number of mixes to DL  {}".format(len(filtered.keys())))
    return filtered

def downloadMixes(htmltext: str):
    '''
    Download all mixes found within the HTML text
    '''
    filtered = extractMixes(htmltext)
    for match in filtered.keys():
        
        # Extract the year from the extracted filename
        year = re.match('^\d{4}', match[1])
        print(year)
        if(year):
            year = year.group(0)
        print(year)

        # Create the year directory if required
        year_dir = createYearDir(year)
        
        # Example URL for downloading
        # http: // download.mixcloud - downloader.com / d / mixcloud / essentialmixcollection / 20180310 - essential - mix - peggy - gou
        
        # Format the download URL
        mcd_url = "{}/{}/".format('http://download.mixcloud-downloader.com/d/mixcloud', match[0])
        
        # Essential mix filename
        emix_file = "{}/{}.mp4".format(year_dir, match[1])
        print("Downloading from : {}".format(mcd_url))
        print("Destination file : {}".format(emix_file))
        if (fileExist(emix_file)):
            print("Skipping {} - reason - already exists".format(emix_file))
            continue

        # Use a temp file to download the mp4 file into before moving 
        # it to the real file after download is complete
        temp_file = "{}.tmp".format(emix_file)

        # Open an http request to Mixcloud
        r = requests.get(mcd_url, stream=True, verify=False)

        # Open the destination .mp4 file
        with open(temp_file, 'wb') as MP4:
            # Download the mp4 file and stream by chunks to file
            for chunk in r.iter_content(chunk_size=1024):
                # writing one chunk at a time to pdf file
                if chunk:
                    MP4.write(chunk)
        
        # Rename the temp file to the real filename 
        os.rename(temp_file, emix_file)


def main( argv ):
    '''
    
    Main Mixcloud downloader routine
    Args:
        argv: system arguments
    Returns: False
    
    '''
    print("Mixcloud mix downloader")

    # Set all years for the essentialmix
    years = [ y for y in range(1993,2020,1) ]
    years_hash = { y:'essential-mix-'+str(y) for y in years}
    # Test a single year
    #years_hash[1993] = ''
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
    main( sys.argv )