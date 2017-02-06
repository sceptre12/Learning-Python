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