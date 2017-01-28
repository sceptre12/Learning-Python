#!/usr/bin/python
import urllib2;
from bs4 import BeautifulSoup;
class ArrayFunctions:
        
    @staticmethod
    def map(func,list):
        newList = [];
        for item in list: newList.append(func(item));
        return newList;
        
    @staticmethod
    def filter(func,list):
        newList = [];
        for item in list:
            if (func(item)): 
                newList.append(item);
        return newList;
        
    @staticmethod
    def forEach(func,list,*args): 
        for item in list: func(item,args);
        
    @staticmethod
    def reduce(func,list,initial = None):
        if len(list) == 0: return;
        if len(list) == 1: return list[0];
        if(initial == None): return ArrayFunctions.__reduceInternal(func,list,list[0],list[1]);
        return ArrayFunctions.__reduceInternal(func,list,initial,list[0]);
    
    #Reduce internal function that applies a function against an accumulator and each value of the array (from left-to-right) to reduce it to a single value.
    @staticmethod
    def __reduceInternal(func,list,previous,current):
        tempList = []
        tempList.extend(list);
        #  If there are no more items in the list 
        if len(tempList) == 0 : return previous;
        # if there is only one item in the list
        if len(tempList) == 1 : return ArrayFunctions.__reduceInternal(func,[],func(previous,tempList[0]),None);
        # if there are more than one item in the list 
        if len(tempList) >= 2:
            firstIndex = tempList[0];
            if(firstIndex == previous and current == tempList[1]): 
                firstIndex = current;
                del tempList[0];
            del tempList[0];
            return ArrayFunctions.__reduceInternal(func,tempList,func(previous,firstIndex),tempList[0]);

# Parent class for all the crawlers            
class Crawler(object):
    def __init__(self,path,searchTerms):
        super(Crawler,self).__init__();
        self._path = path;
        self.searchTerms = searchTerms;
        self.html = self._openLink(path);
        self._parser = BeautifulSoup(self.html);
        
    # Returns readable searchTerm List
    def getSearchTerms(self): return tuple(self.searchTerms);
    
    # Get All Link Tags
    # Returns a list of objects
    def _getAllLinks(self): return self._parser.findAll('a');
        
    # Open up page content
    def _openLink(self,path): return urllib2.urlopen(path).read();
    
    # Filters the line that contain the a tag and href links with http|https attr
    def _isExternalLink(self,line): 
        attributes = line.attrs;
        if(attributes.has_key('href')):
            return attributes.get('href').find('http') > -1 or attributes.get('href').find('https') > -1;
        return False;
    
    # Filters the line that contains the a tag and href link with /
    def _isInternalLink(self,line): 
        attributes = line.attrs;
        if(attributes.has_key('href')):
            link = attributes.get('href');
            if(len(link) > 2 and link[0] =='/'):
                if(link[1] != '/'):return True;
        return False;
    
    # Filter Links based on search terms   
    def _filteredLinks(self,link): 
        found = False;
        for word in self.searchTerms:
            if(link.string != None and link.string.lower().find(word) > -1): found = True;
        return found;
        
    # Returns all the links on the current page leading to different domains
    def getExternalLinks(self): return ArrayFunctions.filter(self._isExternalLink,self._getAllLinks()); 
    
    # Get all Internal domain links on the current page
    def getInternalLinks(self): return ArrayFunctions.filter(self._isInternalLink,self._getAllLinks());
    
    # gets the filtered links based on search terms
    def getFilteredLinks(self): return ArrayFunctions.filter(self._filteredLinks,self.getInternalLinks());
        
    # Create Searchable Objects
    # Function is used in a map to construct Objects with specialized information
    def _constructSearachableObjs(self,link):
        return {
            'JobTitle': link.string,
            'url': link.attrs.get('href')
        }
    
    # Gets list of SearchedTermObjects
    def getSeachedTerms(self): return ArrayFunctions.map(self._constructSearachableObjs,self.getFilteredLinks());
        
   


# Crawler for the indeed website
class IndeedCrawler(Crawler):
    def __init__(self,path,searchTerms):
        assert(path.find('indeed.com') > 0), 'This is not a link for indeed';
        super(IndeedCrawler,self).__init__(path,searchTerms);
        self.searchLinks = {};
    
    # Modify the list and return the links and the name of the job
    def getJobAttributes(self,line):
        print line;
        
    # Filter on indeedSpecificJobs
    def filterJobs(self,link):
        return link.find('turnstileLink') > 0 and link.find('<a') > 0;  
        
    # def runSearch(self): return ArrayFunctions.filter(self.filterJobs,self.htmlLines);

# Crawler for the Craigslist website
class CraiglistCrawler(Crawler):
    def __init__(self,path,searchTerms,mainUrl):
        assert (path.find('craigslist.org') > 0), 'This is not a link for craigslist';
        super(CraiglistCrawler,self).__init__(path,searchTerms);
        self.__runAmount = self.__getRunAmount();
        self.searchLinks = [];
        self.pathList = [path];
        self.mainUrl = mainUrl;
        
        
    # Gets the next link
    def __getNextPageLink(self): return self._parser.find('a',class_ = 'next').attrs.get('href');
        
    # Determines how many pages the crawler is going to visit
    def __getRunAmount(self):
        start = self._parser.find(class_ = 'rangeTo').string;
        end = self._parser.find(class_ = 'totalcount').string;
        return  int(end)/ int(start);
        
    # Recursively digs into the craiglist job search
    # and stores important information in a list which is then
    # filtered into several categories
    def digIntoCraigslist(self):
        if(self.__runAmount == 0):return;
        
        # Adding the current search terms into the searchLinks list
        self.searchLinks.extend(self.getSeachedTerms());
        
        # gets the next page link    
        nextPageLink = self.__getNextPageLink();
        if(nextPageLink == ''):return;
        self._parser = BeautifulSoup(self._openLink(self.mainUrl + nextPageLink));
        self.__runAmount -= 1;
        self.digIntoCraigslist();
    
        