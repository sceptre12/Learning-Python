from flask import Flask, request,session
from modules.crawlers import CraigsListCrawler, IndeedCrawler
import os
app = Flask(__name__)

indeedMain = 'https://www.indeed.com'
indeedQuery = indeedMain + '/jobs?l=Orlando,+FL&radius=50&explvl=entry_level'
mainUrl = 'http://orlando.craigslist.org'
path = mainUrl + '/search/jjj'
searchTerms = ['dental','medical','healthcare','corporate','human resource','accounting','account','office','assistant','reception','receiptionist','pediatric','coder','biller']




@app.route('/')
def temp():
    return 'test'

@app.route('/searchTerms', methods=['GET'])
def getSearchTerms():
    return searchTerms

@app.route('/searchTerms',methods=['POST'])
def updateSearchTerms():
    global searchTerms
    '''
        Request.json should be in this format
        {
            replace: 'false|true',
            arr: []
        }
    '''
    searchTermUpdate = request.json
    if(searchTermUpdate['replace']):
        searchTerms = searchTermUpdate['arr']
    else: 
       searchTerms.extend(searchTermUpdate['arr'])
    return searchTerms 

@app.route('/craigslist')
def getCraigsList():
    craigsListCrawler = CraigsListCrawler(path,searchTerms,mainUrl)
    craigsListCrawler.ActivateSearch(False)
    return craigsListCrawler._json.dumps(craigsListCrawler.searchLinks)

@app.route('/indeed')
def getIndeed():
    indeedCrawler = IndeedCrawler(indeedQuery,searchTerms,indeedMain)
    indeedCrawler.ActivateSearch(False)
    return indeedCrawler._json.dumps(indeedCrawler.searchLinks)
    
app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT',8080)))