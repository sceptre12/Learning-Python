# Crawler for the Craigslist website
from ..parent.crawler import Crawler;
class CraigsListCrawler(Crawler):
    def __init__(self,path,searchTerms,mainUrl):
        assert (path.find('craigslist.org') > 0), 'This is not a link for craigslist';
        super(CraigsListCrawler,self).__init__(path,searchTerms,mainUrl);
        self.__runAmount = self.__getRunAmount();
        self.__fileName = self._dataDumpPath + '/craigslistOutput.txt';
        
    # Gets the next link
    def __getNextPageLink(self): return self._parser.find('a',class_ = 'next').attrs.get('href');
        
    # Determines how many pages the crawler is going to visit
    def __getRunAmount(self):
        start = self._parser.find(class_ = 'rangeTo').string;
        end = self._parser.find(class_ = 'totalcount').string;
        return  int(end)/ int(start);
        
    # Activate Craigslist Seach
    def ActivateSearch(self,storeInFileOrNah):
        FileOpener = None;
        if(storeInFileOrNah):
            try:
                FileOpener = open(self.__fileName,'a');
            except IOError:
                print 'Error in opening file';
            # Write to file 
            if(FileOpener != None):
                self.digIntoCraigslist(FileOpener,storeInFileOrNah);
                FileOpener.close();
            else:
                print 'Error';
        else:
            self.digIntoCraigslist(FileOpener,storeInFileOrNah);
        
    # Digs into the craiglist job search
    # and stores important information in a list which is then
    # filtered into several categories
    def digIntoCraigslist(self,FileOpener,storeInFileOrNah):
        while(self.__runAmount != 1):
            if(storeInFileOrNah):
                FileOpener.write(str(self.getSeachedTerms()));
            else:
                # Adding the current search terms into the searchLinks list
                self.searchLinks.extend(self.getSeachedTerms());
            
            # gets the next page link    
            nextPageLink = self.__getNextPageLink();
            if(nextPageLink == ''):return;
            self._parser = self._BeautifulSoup(self._openLink(self.mainUrl + nextPageLink));
            self.__runAmount -= 1;
    
        