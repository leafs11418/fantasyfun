# fantasyfun

Sample of code used to create rankings of qbs and skill position players (rb & wr) from the 2021 season and 2019-2021. 
Decided to rank players by their weekly average fantasy output + by their typical score range (interquartile range) due to many disappointing playoff performances by my team. I want to try drafting a consistent team (high floor) rather than an explosive team (high ceiling). 

Steps: 
- scrape weekly fantasy stats using BeautifulSoup
- Apply league scoring settings to stats
- Figure out IQR using Pandas/numpy and sort 

Sample code for the intial scrape and application of functions included in scrapexample.py
I played around with Bokeh to create some plots from these data points (website folder). 
Ranking lists (csv) are in the "ranks" folder. 
