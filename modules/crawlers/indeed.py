# Crawler for the indeed website
from ..parent.crawler import Crawler;
class IndeedCrawler(Crawler):
    def __init__(self,path,searchTerms,mainUrl):
        assert(path.find('indeed.com') > 0), 'This is not a link for indeed';
        super(IndeedCrawler,self).__init__(path,searchTerms,mainUrl);
        self.__NumOfJobsPerPage = 15;
        self.__runAmount = self.__getRunAmount();
        self.__fileName = './indeedOutput.txt';
        
    # Gets the next page link
    def __getNextPageLink(self): return self._parser.find('span', class_ = 'np').parent.parent.attrs.get('href');
    
    # Determine run Amount
    def __getRunAmount(self): return round(int(self._parser.find('div', id='searchCount').string.split('of')[1].replace(',','')) / self.__NumOfJobsPerPage);
    
    # Activate Indeed Seach
    def ActivateIndeedSearch(self,storeInFileOrNah):
        FileOpener = None;
        if(storeInFileOrNah):
            try:
                FileOpener = open(self.__fileName,'a');
            except IOError:
                print 'Error in opening file';
            # Write to file 
            if(FileOpener != None):
                self.__digIntoIndeed(FileOpener,storeInFileOrNah);
                FileOpener.close();
            else:
                print 'Error';
        else:
            self.__digIntoIndeed(FileOpener,storeInFileOrNah);
    
    # Searches through all job postings 
    def __digIntoIndeed(self,FileOpener,storeInFileOrNah):
        while(self.__runAmount != 1):
            if(storeInFileOrNah):
                FileOpener.write(str(self.getSeachedTerms()));
            else:
                self.searchLinks.extend(self.getSeachedTerms());
            # Gets the next Page link
            nextPageLink = self.__getNextPageLink();
            if(nextPageLink == ''): return;
            self._parser = self._BeautifulSoup(self._openLink(self.mainUrl + nextPageLink));
            self.__runAmount -= 1;
            