#!/usr/bin/python
import urllib2;
from bs4 import BeautifulSoup;
from Classes import ArrayFunctions, CraiglistCrawler, IndeedCrawler;
indeedMain = 'https://www.indeed.com';
indeedQuery = indeedMain + '/jobs?l=Orlando,+FL&radius=50&explvl=entry_level';
mainUrl = 'http://orlando.craigslist.org';
path = mainUrl + '/search/jjj';

# Terms that the crawler homes in on
searchTerms = ['dental','medical','healthcare','corporate','human resource','accounting','account','office','assistant','reception','receiptionist','pediatric','coder','biller'];

craigCrawler = CraiglistCrawler(path,searchTerms,mainUrl);

print str(craigCrawler.getSeachedTerms());
# print craigCrawler.digIntoCraigslist();

# print craigCrawler.searchLinks;

# print ; print ; print ; print ;

# indeedCrawler = IndeedCrawler(indeedQuery,searchTerms,indeedMain);

# # indeedCrawler.ActivateIndeedSearch(True);
# print indeedCrawler.getSeachedTerms();