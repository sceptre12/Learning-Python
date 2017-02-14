from modules.crawlers import CraigsListCrawler, IndeedCrawler;


indeedMain = 'https://www.indeed.com';
indeedQuery = indeedMain + '/jobs?l=Orlando,+FL&radius=50&explvl=entry_level';
mainUrl = 'https://orlando.craigslist.org';
path = mainUrl + '/search/jjj';

# Terms that the crawler homes in on
searchTerms = ['dental','medical','healthcare','corporate','human resource','accounting','account','office','assistant','reception','receptionist','pediatric','health first','dentistry'];
craigCrawler = CraigsListCrawler(path,searchTerms,mainUrl);

craigCrawler.ActivateSearch(False);
print craigCrawler._json.dumps(craigCrawler.searchLinks);

# print ; print ; print ; print ;

# indeedCrawler = IndeedCrawler(indeedQuery,searchTerms,indeedMain);

# indeedCrawler.ActivateSearch(True);