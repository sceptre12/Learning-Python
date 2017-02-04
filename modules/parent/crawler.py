from bs4 import BeautifulSoup;
from utils import ArrayFunctions;
import urllib2;
import json;
# Parent class for all the crawlers            
class Crawler(object):
    def __init__(self,path,searchTerms,mainUrl):
        super(Crawler,self).__init__();
        self._path = path;
        self.mainUrl = mainUrl;
        self.searchTerms = searchTerms;
        
        self._json = json;
        self._BeautifulSoup = BeautifulSoup;
        self._urllib2 = urllib2;
        self.searchLinks = [];
        self.html = self._openLink(path);
        self._parser = self._BeautifulSoup(self.html);
        
        
    # Returns readable searchTerm List
    def getSearchTerms(self): return tuple(self.searchTerms);
    
    # Get All Link Tags
    # Returns a list of objects
    def _getAllLinks(self): return self._parser.findAll('a');
        
    # Open up page content
    def _openLink(self,path): return self._urllib2.urlopen(path).read();
    
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
        return self._json.dumps({
            "JobTitle": link.string.encode('utf-8').strip(),
            "url": link.attrs.get('href').encode('utf-8').strip()
        });
    
    # Gets list of SearchedTermObjects
    def getSeachedTerms(self): return ArrayFunctions.map(self._constructSearachableObjs,self.getFilteredLinks());
        
 