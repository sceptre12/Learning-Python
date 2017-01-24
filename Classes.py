#!/usr/bin/python
import urllib2;
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

    
class CraiglistCrawler(ArrayFunctions):
    def __init__(self,path,searchTerms):
        self.__searchTerms = searchTerms;
        self.__path = path;
        self.__htmlLines =  self.__openLink(path);
        self.__runAmount = self.__determineHowManyPages(self.__htmlLines);
        self.searchLinks = {};
        self.itemLinks = {};
        self.pathList = [path];
        
    # Open up links
    def __openLink(self,path): return urllib2.urlopen(path).read().splitlines();
    
    # Returns readable searchTerm List
    def getSearchTerms(self): return tuple(self.__searchTerms);
    # Returns the url path
    def getPath(self): return self.__path;
    # Returns the list of searchable links
    def getSearchLinks(self): return self.searchLinks;
    # Returns the list of items matching search terms
    def getItemLinks(self): return self.itemLinks;
        
    # Filters the line that contain the a tag and href links with http|https attr
    def __isExternalLink(self,line): return line.find('<a') > 0 and (line.find('href="http') > 0 or line.find('href="https') > 0);
    
    # Filters the line that contains the a tag and href link with /
    def __isInternalLink(self,line): return line.find('<a') > 0 and (line.find('href="/') > 0);
    
    # Maps and Trims the line and returns the href content
    def __trimLine(self,line): 
            line.strip();
            start = line.find('href="') + 6;
            line = line[start:len(line)];
            
            end1 = line.find('">');
            end2 = line.find('" ');
            
            if(end1 < 0): return line[:end2];
            if(end2 < 0): return line[:end1];
            
            if (end1 < end2):
                return line[:end1];
            elif(end2 < end1): 
                return line[:end2];
                
    # Filter Links based on search terms   
    def __filteredLinks(self,links): 
        found = False;
        for word in self.__searchTerms:
            if(links.find(word) > 0 and links.find('<a') > 0): found = True;
        return found;
    
    # Gets the next link
    def __getNextPageLink(self,links):
        nextPageLink = '';
        for link in links:
            if(link.find('next') > 0): nextPageLink = self.__trimLine(link); break;
        return nextPageLink;
        
    #Filters out the unnecessary fields
    def __craigslistFilterUnecessary(self,line): return line.find('craigslist') == -1 and len(line) != 1;
        
    # Determines how deep the crawler should navigate
    def __determineHowManyPages(self,lines):
        currentLine = 0;
        index = 0;
        for item in lines: 
            if(item.find('rangeTo') > 0): currentLine = index; break;
            index +=1;
        line = lines[currentLine];
        rangeTo = line[line.find('rangeTo') + 9:];
        start = int(rangeTo[:rangeTo.find('</')]);
        totalCount = line[line.find('totalcount') + 12:];
        end = int(totalCount[:totalCount.find('</')]);
        return round(end / start);
    
    # Returns all the links on the current page leading to different domains
    def getExternalLinks(self): return self.map(self.__trimLine,self.filter(self.__isExternalLink,self.__htmlLines)); 
    
    # Get all Internal domain links on the current page
    def getInternalLinks(self): return self.filter(self.__craigslistFilterUnecessary,self.map(self.__trimLine,self.filter(self.__isInternalLink,self.__htmlLines)));
    
    # gets the filtered links based on search terms
    def __getFilteredLinks(self): return self.map(self.__trimLine,self.filter(self.__filteredLinks,self.__htmlLines));
        
    # Recursively digs into the craiglist job search
    # and stores important information in a list which is then
    # filtered into several categories
    def digIntoCraigslist(self):
        if(self.__runAmount == 1):
            return{
                'searchLinks': self.searchLinks,
                'itemLinks': self.itemLinks
            }
        filteredResults = self.__getFilteredLinks();
        
        # Filters out the internal links from the important links
        for result in filteredResults:
            if(result.find('search') > 0):
                if(self.searchLinks.has_key(result) == False):
                    self.searchLinks[result] = 1;
            else:
                if(self.itemLinks.has_key(result) == False):
                    self.itemLinks[result] = 1;
        
        # gets the next page link    
        nextPageLink = self.__getNextPageLink(self.__htmlLines);
        if(nextPageLink == ''):
            return{
                'searchLinks': self.searchLinks,
                'itemLinks': self.itemLinks
            }
        self.__htmlLines = self.__openLink(nextPageLink);
        self.__runAmount -= 1;
        self.digIntoCraigslist();
    
    def convertedSiteUrl(self,mainUrl): 
        def changeToFullUrl(item):return mainUrl + item;
        return self.map(changeToFullUrl,self.itemLinks.keys());
        