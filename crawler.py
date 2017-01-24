#!/usr/bin/python
import urllib2;
from Classes import ArrayFunctions, CraiglistCrawler;
mainUrl = 'http://orlando.craigslist.org';
path = mainUrl + '/search/jjj';

# Terms that the crawler hones in on
searchTerms = ['dental','medical','healthcare','corporate','human resource','accounting','account','office','assistant','reception','receiptionist','pediatric','coder','biller'];

crawler = CraiglistCrawler(path,searchTerms);

print crawler.digIntoCraigslist()

print str(crawler.searchLinks)

print str(crawler.itemLinks)

print str(crawler.convertedSiteUrl(mainUrl))
