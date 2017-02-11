from flask import Flask
from modules.crawlers import CraigsListCrawler, IndeedCrawler;
import os
app = Flask(__name__)

indeedMain = 'https://www.indeed.com';
indeedQuery = indeedMain + '/jobs?l=Orlando,+FL&radius=50&explvl=entry_level';
mainUrl = 'http://orlando.craigslist.org';
path = mainUrl + '/search/jjj';
searchTerms = ['dental','medical','healthcare','corporate','human resource','accounting','account','office','assistant','reception','receiptionist','pediatric','coder','biller'];
craigsListCrawler = CraigsListCrawler(path,searchTerms,mainUrl);


@app.route('/')
def temp():
    return 'test'

@app.route('/run')
def hello_world():
    craigsListCrawler.ActivateSearch(False)
    return craigsListCrawler.searchLinks

app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT',8080)))