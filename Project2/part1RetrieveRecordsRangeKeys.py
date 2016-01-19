from bsddb3 import db
from datetime import datetime
import random
    
def rangeSearch(datb, keyS, keyE):
    """Retrieve records with a given range of key values
    Keyword arguments:
    datb -- the database.
    keyS -- starting key.
    keyE -- ending key.
    Returns a list of key/data pair within the range, inclusive.
    """    
    rangeFind = list()
    cur = datb.cursor()
    
    if datb.get_type() == 2:
        #puts cursor to last place and gets its data
        ends = cur.last()
        #Puts cursor back to the first place gets its data, starting the search from here now.
        z = cur.first()
        
        while(True):
            if (z[0] <= keyE and z[0] >= keyS):
                rangeFind.append(z)
            
            z = cur.next()
            
            if(z == ends):
                break;
        #expensive tooo??? might do it outside this function?:
        #rangeFind.sort()
            
    elif datb.get_type() == 1:
        z = cur.set_range(keyS)
        
        while(z[0] <= keyE):
            rangeFind.append(z)
            z = cur.next()
        
    cur.close()
    return rangeFind
  
def stopTime(currentTime ):
    """Stops time itself.
    Keyword arguments:
    currentTime -- the starting time.
    Returns the amount of microseconds in a list, 1st index: text friendly format, 2nd index: pure number.
    """
    stopTime = datetime.now()
    elapsedTime = stopTime - currentTime
    microsecs = elapsedTime.microseconds

    #print("The total time elapsed in microseconds was : %s" %(str(microsecs)))
    
    return ["The total time elapsed in microseconds was : %s\n" %(str(microsecs)), microsecs]
    
def randKeyList(datb, num):
    """ Gets n random starting and ending keys from a database and returns a list of n starting and ending keys tuple.
    Keyword arguments:
    datb -- the database
    num -- the number of starting & ending keys to get.
    """
    keyList = datb.keys()
    randKeys = list()
    for i in range(num):
        keyAlot= len(keyList)-201
           
        keySt = random.choice(keyList[:(keyAlot)])
       
        randIndex = keyList.index(keySt) + random.randint(100,200)
        keyEd = keyList[randIndex]
        randKeys.append((keySt,keyEd))
            
    return randKeys
    
def counting(dbB, keyLists):
    """Times 4 random range searches between 100-200 records and gets an average of those 4 tests.
    This silly function REQUIRES Btree to be opened first. (So it can get the random keys from a sorted database!)
    Keyword arguments:
    typ -- the type of database that should be tested (either Hash Table or B+Tree).
    Returns a list containing a list [key, value, "\n", ... ]
    """
    #db.get_type(), return 1 if BTree, returns 2 if Hash
    #print(dbB.get_type())
    theLines = []
    timedCalc = []
    total = 0
            
    for i in range(4):                
        
        currentTime = datetime.now()
        rangedList = rangeSearch(dbB, keyLists[i][0], keyLists[i][1])
        microSec = stopTime(currentTime)
        
        timedCalc.append(microSec[1])    
        
        if(dbB.get_type() == 2):
            typ = "Hash Table"
            rangedList.sort()
            
        elif(dbB.get_type() == 1):
            typ = "B+Tree"
        
        print("  %s Trial %d" %(typ, i+1))
        print("    Starting Key: "+keyLists[i][0].decode(encoding='UTF-8'))
        print("    Ending Key: "+keyLists[i][1].decode(encoding='UTF-8'))
        print("    Records within that range found: %d" %len(rangedList))
        print("    %s"%microSec[0])
        #print("    The key data pairs found:", rangedList)
        
        #writed.writelines([  ("%s Trial %d\n" %(typ, i+1)), ("  Starting Key: "+keyLists[i][0].decode(encoding='UTF-8')+"\n"), 
        #                        ("  Ending Key: "+keyLists[i][1].decode(encoding='UTF-8')+"\n"), 
        #                        ("  Records within that range found: %d\n" %len(rangedList)), "  %s\n"%microSec[0] ] )
        
        for each in rangedList:
            theLines.append("%s\n" %each[0].decode())
            theLines.append("%s\n" %each[1].decode())
            theLines.append("\n")
        
    for each in timedCalc:
        total += each
        
    total /=  len(timedCalc)
    print("Average time for testing %s was %d microseconds.\n\n"%(typ, total))
    #writed.writelines("Average time for testing %s was %d microseconds.\n\n"%(typ, total))
    
    return theLines  
    
def main():
    dbB = db.DB()
    dbH = db.DB()
    
    dbBtree = "part1BT"
    dbB.open(dbBtree, None, db.DB_BTREE, db.DB_CREATE)
    keys = randKeyList(dbB, 4)
        
    dbHash = "part1HT"
    dbH.open(dbHash, None, db.DB_HASH, db.DB_CREATE)
    
    answers = open("part1RangedAnswers.txt","w")
    
    print("Performing B+Tree tests...")
    theLines = counting(dbB, keys)
    answers.writelines(theLines)
    
    print("Performing Hash Table tests...")
    theLines = counting(dbH, keys)
    answers.writelines(theLines)
    
    print("Done. See part1RangedAnswers.txt")
    dbB.close()
    dbH.close()
    answers.close()

if __name__ == "__main__":
    main()
    
