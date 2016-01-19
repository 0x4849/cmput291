import sys
import random
import bsddb3
from bsddb3 import db
#import time
from datetime import datetime

class P2Tests:
  def __init__(self):
    self.answers = open("part1keyanswers.txt", "w")
    
    self.db1Path = "part1BT"
    self.db2Path = "part1HT"
    self.db3Path = "indexfile"
    self.db3 = db.DB()

    self.db1MicroSeconds = []
    self.db1MilliSeconds = []
    
    self.db2MicroSeconds = []
    self.db2MilliSeconds = []

    self.db3MicroSeconds = []
    self.db3MilliSeconds = []
    
    self.db1 = bsddb3.btopen(self.db1Path, 'c')
    self.db2 = bsddb3.hashopen(self.db2Path, 'c')
    self.db3.open(self.db3Path, None, db.DB_HASH, db.DB_CREATE)
   # self.db1.open(self.db1Path, None, db.DB_BTREE, db.DB_CREATE)
   # self.db2.open(self.db2Path, None, db.DB_HASH, db.DB_CREATE)
   # self.db3.open(self.db3Path, None, db.DB_BTREE, db.DB_CREATE)

    self.mainMenu()
   
  def mainMenu(self):
      print("\nRunning Retrieve Key Given Record.")
      self.retrieveKeyRecord()
      
  def retrieveKeyRecord(self):
    for i in range(4):
      key = random.choice(self.db1.keys())
      record = self.db1[key]

      
      print("\nThe following record has been randomly selected from the database "+str(record))
      print("\nRetrieving key(s) pertaining to this record. Testing against BTree")
    
      self.recordTime()
      data = self.retrieveKey2(record)
      theTime = self.stopTime(self.db1MicroSeconds, self.db1MilliSeconds)
            
      print("\nThe keys returned were "+str(data))
      #self.recordAnswer([theKey+"\n",theData+"\n",theTime+"\n","\n"])
      #print('\n\n\n',data)
      self.recordAnswer(data, theTime)
      
      print("\nRetrieving key pertaining to this record. Testing against HTable")
      self.recordTime()
      data = self.retrieveKey1(record)
      theTime = self.stopTime(self.db2MicroSeconds, self.db2MilliSeconds)
      
      print("\nThe keys returned were: "+str(data))
      self.recordAnswer(data, theTime)
      #self.recordAnswer([theKey+"\n", theData+"\n","\n"])
      print("\nRetrieving key pertaining to this record.Testing against IndexFile")
      self.recordTime()
      record = self.retrieveKey3(record)
      theTime = self.stopTime(self.db3MicroSeconds, self.db3MilliSeconds) 
      print("\nThe keys returned were: "+str(data))
      self.recordAnswer(data, theTime) 

    db1Micro = sum(self.db1MicroSeconds)/len(self.db1MicroSeconds)
    db1Milli = sum(self.db1MilliSeconds)/len(self.db1MilliSeconds)
    
    db2Micro = sum(self.db2MicroSeconds)/len(self.db2MicroSeconds)
    db2Milli = sum(self.db2MilliSeconds)/len(self.db2MilliSeconds)

    db3Micro = sum(self.db3MicroSeconds)/len(self.db3MicroSeconds)
    db3Milli = sum(self.db3MilliSeconds)/len(self.db3MilliSeconds) 
    
    print("Total average time elapsed for BTree in micro seconds was "+str(db1Micro))
    print("Total average time elapsed for BTree in milli seconds was "+str(db1Milli))
    print("Total average time elapsed for HashTable in micro seconds was "+str(db2Micro))
    print("Total average time elapsed for HashTable in milli seconds was "+str(db2Milli))
    print("Total average time elapsed for IndexFile in micro seconds was "+str(db3Micro))
    print("Total average time elapsed for IndexFile in milli seconds was "+str(db3Milli))
  
    self.recordAnswerTime(["\n BTree's average time in micro seconds was : "+str(db1Micro)+"\n","\n In milliseconds it was : "+str(db1Milli)+"\n","\n HashTable's average time in micro seconds was : "+str(db2Micro)+"\n In milliseconds it was : "+str(db2Milli)+"\n","\n IndexFile's average time in micro seconds was : "+str(db3Micro)+"\n","\n In milliseconds it was : "+str(db3Milli)+"\n"])

    self.quit()
  
  def retrieveKey1(self, record):
    result_set = []
    last_item = self.db2.last()
    db_item = self.db2.first()
    while True:
      if db_item[1] == record:
        result_set.append(db_item)
      if db_item == last_item:
        break
      else:
        db_item = self.db2.next()
    return result_set
      
  def retrieveKey2(self, record):
    result_set = []
    last_item = self.db1.last()
    db_item = self.db1.first()
    while True:
      if db_item[1] == record:
        result_set.append(db_item)
      if db_item == last_item:
        break
      else:
        db_item = self.db1.next()
    return result_set
  
  def retrieveKey3(self, record):
    result_set = []
    key = self.db3[record] 
    curs = self.db3.cursor()
    result_set.append(key)
    curs.set(record)
    
    while True:
      #print(curs.next_dup())
      if curs.next_dup():
        result_set.append(curs.current()[::-1])
      else:
        break
    return result_set
  
  def recordTime(self):
    self.currentTime = datetime.now()
  
  def stopTime(self,listToAppend1, listToAppend2):
    stopTime = datetime.now()
    #elapsedTime = self.currentTime - stopTime
    elapsedTime = stopTime - self.currentTime
    microsecs = elapsedTime.microseconds
    millisecs = microsecs * 1000

    print("The total time elapsed in microseconds was : %s" %(str(microsecs)))
    listToAppend1.append(microsecs)
    print("The total time elapsed in milliseconds was : %s" %(str(millisecs)))
    listToAppend2.append(millisecs)
    
    return str(microsecs)
  #Given textToWrite such as : textToWrite = ["a line of text", "another line of text", "a third line"]
  def recordAnswer(self,textToWrite, theTime):
    for i in textToWrite:
      self.answers.writelines(str(i[0])+'\n')
      self.answers.writelines(str(i[1])+'\n')
      self.answers.writelines('\n')
    #self.answers.writelines(textToWrite)
  def recordAnswerTime(self, textToWrite):
      self.answers.writelines(textToWrite) 
  def cleanUpBinary(self,value):
    firstPivot = value.find("'")
    return value[firstPivot:]
  
  def quit(self):
    self.answers.close()
    sys.exit()

testData = P2Tests()

