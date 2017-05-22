# nifty_scrapper
Nifty web scraper

web app where Data must be scrapped every 5 mins from a URL and display
it in Card Layout.
What is Expected:
1. Build a stand-alone web app using any Python Framework
2. Scrape the 'Nifty 50' table (URL in Point 3) values every 5 minutes (in the background and on a different
thread) and persist in a Redis instance.
3. URL:
http://www.nseindia.com/live_market/dynaContent/live_analysis/top_gainers_losers.htm?cat=G
4. On the webapp, display the values stored in Redis in a cards layout (unlike the original table). Use valid
HTML5 + CSS3 to make the view look nice
(eg: http://www.sketchappsources.com/resources/source-image/messages-cards-rahulbhadauria.png)
