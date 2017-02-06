from modules.crawlers import CraigsListCrawler, IndeedCrawler;


indeedMain = 'https://www.indeed.com';
indeedQuery = indeedMain + '/jobs?l=Orlando,+FL&radius=50&explvl=entry_level';
mainUrl = 'http://orlando.craigslist.org';
path = mainUrl + '/search/jjj';

# Terms that the crawler homes in on
searchTerms = ['dental','medical','healthcare','corporate','human resource','accounting','account','office','assistant','reception','receiptionist','pediatric','coder','biller'];
craigCrawler = CraigsListCrawler(path,searchTerms,mainUrl);

# print str(craigCrawler.getSeachedTerms());
craigCrawler.ActivateSearch(True);


# print ; print ; print ; print ;

# indeedCrawler = IndeedCrawler(indeedQuery,searchTerms,indeedMain);

# indeedCrawler.ActivateIndeedSearch(True);