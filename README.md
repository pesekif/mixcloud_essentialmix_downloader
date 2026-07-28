# mixcloud_essentialmix_downloader

Being a fan of the BBC Essential Mix throughout the years I wanted to pull down the whole EM archive that had been placed in Mixcloud under the essentialmix user. The problem is that there is no single list to download from as you need to continually scroll down the web page to gather the mixes in chronological order. To overcome this I built a very simple script utilising  Python Selenium, Requests  and Threading to connect to the Mixcloud website and periodically scroll down the web page to expose all the EM links in the web page (just like a user would) to then download the mp4 URLs once exposed in the html. It takes a while but it does get them eventually.

**Note**
As of 2026 the Essential Mix account no longer exists in Mixcloud so elements of this script no longer works.  I am currently looking for another Mixcloud account that could provide these EM tracks.