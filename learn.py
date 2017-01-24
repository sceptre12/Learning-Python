#!/usr/bin/python
from Classes import ArrayFunctions; 

def testFunc(num,stri,list):
    temp = ''
    for x in list : temp+=str(x);
    print str(num) + stri + temp;
    return

testFunc(1,'tes',[45,7,1,34,45,5]);



testMap = [24,34,53,123];

print 'Data'
print str(testMap);

# function for mapping
def createObj(item):
    return {
        'id': item,
        'type': 'obj'
    }

# function for filtering    
def greaterthanfifty(item): return item['id'] > 50;
# function for reduce 
def addUpItems(item,item2): return item + item2;


print 'MAP'
temp = ArrayFunctions.map(createObj,testMap);

for item in temp: print str(item);

print 'FILTER'
temp = ArrayFunctions.filter(greaterthanfifty,temp);

for item in temp: print str(item);

print 'REDUCE with initial value'

temp = ArrayFunctions.reduce(addUpItems,testMap,10);

print temp;

print 'REDUCE without initial value'

temp = ArrayFunctions.reduce(addUpItems,testMap);

print temp;