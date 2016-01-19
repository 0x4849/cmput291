import sys
import random
import bsddb3
from bsddb3 import db
#import time
from datetime import datetime
import os

#---------------------------------------------------------------
# Project:              2
# Due Date:             April 8th, 2014
# Name:                 Brad Harrison, Emmett Underhill, Ryan Satyabrata
# Lecture Section:      B1
# Instructor:           Li Yuan
# Lab Section:          Monday 1230 - 1400)
# Teaching Assistant:   Thorey Mariusdottir
#---------------------------------------------------------------

class P2Tests:
  def __init__(self):
    #This is the DB Type chosen already. It will be "btree", "hash", or "indexfile"
    #duplicateDB = dict()
    if len(sys.argv) >= 1:
      self.DBType = sys.argv[1] 
    self.answers = open("answers", "w")
    #self.answers = open("answers.txt", "w")
    
    self.db1 = bsddb3.db.DB()
    if self.DBType == 'indexfile':
      self.db2 = bsddb3.db.DB()

    self.createdDB = False
    self.createMenu = False

    #self.items = ["cat", "dog", "cat", "zebra","cat","dog"]
    #self.valuesList = []
    
    #change bpharris_db later to one of our names as mentioned in project page
    if(not os.path.isdir("./tmp/bpharris_db")):
      print("Directory ./tmp/bpharris_db created")
      os.makedirs("./tmp/bpharris_db")
    
    self.mainMenu()
   

  def mainMenu(self):
    print("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("Welcome to the Menu for the Project 2 Tests.") 
    print("The following six options may be selected :")
    print("1 : Create and Populate a Database")
    print("    Information:\n    This option will create and populate the database(s) with random [key, data] pairs.")
    print("\n2 : Retrieve Records with a Given Key")
    print("    Information:\n    This option will retrieve a random record from the database given a key, and the record will be appended into a file named answers in the local directory.")
    print("\n3 : Retrieve Records with a Given Data")
    print("    Information:\n    This option will retrieve a random record from the database given data, and the record will be appended into a file named answers in the local directory.")
    print("\n4 : Retrieve Records with a Given Range of Key Values")
    print("    Information:\n    This option will retrieve a range of records from the database given a key, and the records will be appended into a file named answers in the local directory.")
    print("\n5 : Destroy the Database")
    print("    Information:\n    This option will destroy the database(s) already created.")
    print("\n6 : Quit.")
    print("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------")  
      
    yourChoice = input("Please enter your choice now. Possible choices are : 1, 2, 3, 4, 5, 6 \n")
    yourChoice = yourChoice.lower()
    while yourChoice != '1' and yourChoice != '2' and yourChoice != '3' and yourChoice != '4' and yourChoice != '5' and yourChoice != '6':
      print("Invalid choice.")
      yourChoice = input("Please enter your choice now. Possible choices are : 1, 2, 3, 4, 5, 6 \n")
      yourChoice = yourChoice.lower()
     
    if yourChoice == '1':
      self.createMenu = True
      self.createDB()
        
    elif yourChoice == '2':
      self.retrieveRecordKey()
        
    elif yourChoice == '3':
      self.retrieveRecordData()
        
    elif yourChoice == '4':
      self.rangedSearch()
        
    elif yourChoice == '5':
      self.destroyDB()
        
    elif yourChoice == '6':
      self.quit()
      
  def get_random(self):
    return random.randint(0, 63)

  def get_random_char(self):
    return chr(97 + random.randint(0, 25))
  
  def createDB(self):
    DA_FILE = "./tmp/bpharris_db/sample_db"
    DA_FILE2 = "./tmp/bpharris_db/indexfile"
    #DA_FILE2 = "./index9999"
    DB_SIZE = 100000
    SEED = 10000000
    currentVal = 0
    
    databaseType = self.DBType
    if databaseType == 'indexfile':
      try:
          db = bsddb3.btopen(DA_FILE, "n")
      except:
          print("DB doesn't exist, creating a new one")
          db = bsddb3.btopen(DA_FILE, "c")
      try:
          db2 = bsddb3.hashopen(DA_FILE2, "n")
      except:
          print("DB2 doesn't exist, creating a new one")
          db2 = bsddb3.hashopen(DA_FILE2, "c")
    
    elif databaseType == 'hash':
      try:
          db = bsddb3.hashopen(DA_FILE, "n")
      except:
          print("DB doesn't exist, creating a new one")
          db = bsddb3.hashopen(DA_FILE, "c")
    
    elif databaseType == 'btree':
      try:
          db = bsddb3.btopen(DA_FILE, "n")
      except:
          print("DB doesn't exist, creating a new one")
          db = bsddb3.btopen(DA_FILE, "c")
    
    
    random.seed(SEED)

    for index in range(DB_SIZE):
        krng = 64 + self.get_random()
        key = ""
        for i in range(krng):
            key += str(self.get_random_char())
        vrng = 64 + self.get_random()
        value = ""
        for i in range(vrng):
            value += str(self.get_random_char())
        key = key.encode(encoding='UTF-8')
        value = value.encode(encoding='UTF-8')
        if key not in db:
          db[key] = value
          if databaseType == 'indexfile':
            #If the value already exists in the indexfile --> call customPut to insert duplicate data!
            if value in db2:
              self.customPut(db2,value, key)
            else:
              db2[value] = key
          currentVal += 1
        print("Creating the database: %d%% completed." %((currentVal/DB_SIZE) * 100), end="\r")
        sys.stdout.flush()
    print("Creating the database: 100% completed.")
    try:
        print("Created an %s based database" %(databaseType))
        db.close()
    except Exception as e:
        print (e)
    
    if databaseType == 'indexfile':
      try:
        db2.close()
      except Exception as e:
        print (e)
    
    self.openDatabases()
    
    if(self.createMenu ):
      self.createMenu  = False
      self.mainMenu()
    
  """
  Primarily called after generating databases, but may also be called if a user went to a non-generate DB function before generating a DB.
  Essentially it opens Dbs in this manner:
  Primary DB is always ./tmp/bpharris_db/sample_db
  Secondary DB is always ./tmp/bpharris_db/indexfile
  """
  
  def openDatabases(self):  
    self.createdDB = True
  
    firstDBLocation = "./tmp/bpharris_db/sample_db"

    if self.DBType == 'indexfile':
      secondDBLocation = "./tmp/bpharris_db/indexfile"
      #secondDBLocation = "./indexfile999"
    if self.DBType == 'btree':
      self.db1.open(firstDBLocation, None, db.DB_BTREE, db.DB_CREATE)
    
    elif self.DBType == 'hash':
      self.db1.open(firstDBLocation, None, db.DB_HASH, db.DB_CREATE)
    
    if self.DBType == 'indexfile':
      self.db1.open(firstDBLocation, None, db.DB_BTREE, db.DB_CREATE)
      self.db2.open(secondDBLocation, None, db.DB_HASH, db.DB_CREATE)
    print(len(self.db1))
    print("The database(s) have been opened.\n")


  """
  This function helps create the indexfile. Assuming that a piece of value is already in the indexfile,
  then customPut will do db3[data] = db3[key] concatenated with || and then concatenated with the newest key.
  Of course, in an indexfile, it is viewed as db3[key] = db3[key]+||+data, so that is the way it is represented in the function.
  """
  def customPut(self, db3, key, data):
      #print("HEREEEEEEEEEEEEe")
      keyToAppend = str(db3[key].decode())+"||"+str(data)
      db3[key] = keyToAppend
  
  """In this program, a key is inputted from the user.
  Then, the record is retrieved through key access in the Primary Database,
  and a time is recorded in microseconds for the duration of this record retrieval.
  """
  def retrieveRecordKey(self):
    self.answersOpen()
    if self.createdDB == False:
      yourChoice = input("DBs were not created. Press c to create them, else press o to try to open them.")
      if yourChoice == 'c':
        self.createDB()
      elif yourChoice == 'o':
        self.openDatabases()
    #for i in range(10):
    #  print(random.choice(self.db1.keys()))
    key = input("Input the key that you want to do a key search on.\n")
    print("\nThe following key has been randomly selected from the database "+str(key))
    key = key.encode()
    if key not in self.db1:
      print("\nThe key was not found in the database. Returning to menu now.")
      self.mainMenu()
    print("\nRetrieving record pertaining to this key now.")
    
    self.recordTime()
    record = self.retrieveRecord2(key)
    self.stopTime()
    
    theKey = self.cleanUpBinary(record[0])
    theData = self.cleanUpBinary(record[1])

    print("\nThe record returned was Key: "+str(theKey)+" and Data "+str(theData))
    
    self.recordAnswer([theKey+"\n", theData+"\n","\n"])
    self.answers.close()
    self.mainMenu()
    
  def retrieveRecord2(self,key):
    
    return str(key),str(self.db1.get(key))
    return record

  def answersOpen(self):
    self.answers = open("answers","a")
    
  """
  Asks user for data to search for records with said data.
  if the database being tested is an indexfile, calls retrieveKey3 function
  else, calls retrieveKeyDataOther function, which perform the query on the 
  corresponding database (retrieveKey3 -> indexfile, retrieveKeyDataOther->hash, btree)
  prints the list of resulting records
  """
  def retrieveRecordData(self):
    self.answersOpen()
    if self.createdDB == False:
      yourChoice = input("DBs were not created. Press c to create them, else press o to try to open them.")
      if yourChoice == 'c':
        self.createDB()
      elif yourChoice == 'o':
        self.openDatabases()
    
    #record = random.choice(self.db2.keys())
    #record = random.choice(self.items)
    #record = record.encode()
    theInput = input("Please enter a piece of data to retrieve a record from.\n")
    #print("\nThe following record has been randomly selected from the database "+str())
    print("\nRetrieving key pertaining to this record now.")
    record = theInput.encode()
    if self.DBType == 'indexfile': 
      self.recordTime()
      #data = self.retrieveKeyDataIndex(record)
      data = self.retrieveKey3(record)
      self.stopTime()
    else:
      self.recordTime()
      data = self.retrieveKeyDataOther(record)
      self.stopTime()
   
    print("\nThe records returned were:",data)
    self.recordAnswerIndex(data)
    self.answers.close()
    self.mainMenu() 

  def rangeSearch(self, datb, keyS, keyE):
    """Retrieve records with a given range of key values
    Keyword arguments:
    datb -- the database.
    keyS -- starting key.
    keyE -- ending key.
    Returns a list of key/data pair within the range, inclusive.
    """    
    rangeFind = list()
    cur = datb.cursor()
    #puts cursor to last place and gets its data
    ends = cur.last()
    if datb.get_type() == 2:
      #Puts cursor back to the first place gets its data, starting the search from here now.
      currKey = cur.first()
      
      while(True):
        if(type(currKey) == type(None)):
          print("Error: None type found. An invalid key may have been inputted or DB is corrupt/empty.")
          return rangeFind
        if (currKey[0] <= keyE and currKey[0] >= keyS):
          rangeFind.append(currKey)
          
        currKey = cur.next()
            
        if(currKey == ends):
          rangeFind.append(currKey)
          break;
          
        #rangeFind.sort()#expensive tooo??? might do it outside this function?:
            
    elif datb.get_type() == 1:
      currKey = cur.set_range(keyS)
      if(type(currKey) == type(None)):
        print("Error: None type found. An invalid key may have been inputted or Database may be empty or corrupt.")
        return rangeFind
      while(currKey[0] <= keyE):
        if(type(currKey) == type(None)):
          print("Error: None type found. An invalid key may have been inputted or Database may be empty or corrupt.")
          return rangeFind
        rangeFind.append(currKey)
        currKey = cur.next()
        if(currKey == ends):
          rangeFind.append(currKey)
          break
        
    cur.close()
    return rangeFind
  """
  Performs a sequential search on the database, looks at each
  record and appends the record to the result_set list if the record
  data matches the query data. The result set is returned
  """
    
  def retrieveKeyDataOther(self, record):
    result_set = []
    curs = self.db1.cursor()
    last_item = curs.last()
    db_item = curs.first()
    while True:
      #print(record, db_item[1])
      if db_item[1] == record:
        result_set.append(db_item)
      if db_item == last_item:
        break
      else:
        db_item = curs.next()
    curs.close()
    return result_set

  """
  This function returns record(s) given a piece of data from an indexfile DB.
  It simply performs a get(data) function call on the indexfile, which results in [data] = key1||key2||key3.
  A python list split function is called, which splits the string into a list separated by || delimiters,
  and then these lists are then parsed into the proper format for record answers.
  """
  def retrieveKey3(self,key):
    if key not in self.db2:
      print("\nThe key was not found in the indexfile. Returning to main menu now.")
      self.mainMenu()
    result_set = []
    listOfKeys = self.db2.get(key)
    self.stopTime()
    listOfKeys = listOfKeys.decode()
    listOfKeys = listOfKeys.replace("b'","")
    listOfKeys = listOfKeys.replace('''"''','')
    listOfKeys = listOfKeys.replace("'","")
    
    key = key.decode()
    listOfKeys = listOfKeys.split("||")
    newList = []
    for index in listOfKeys:
      newList.append((index, key))
    return newList


  def rangedSearch(self):
    """Gets starting key and ending key and then calls rangeSearch function 
    and times it and will write records found in range to answers file, and
    prints the number of records found and the time it took.
    """
    self.answersOpen()
    
    if self.createdDB == False:
      yourChoice = input("DBs were not created. Press c to create them, else press o to try to open them.")
      if yourChoice == 'c':
        self.createDB()
      elif yourChoice == 'o':
        self.openDatabases()
   
    keySt = input("Please enter starting key:\n").encode(encoding='UTF-8')
    keyEd = input("Please enter ending key:\n").encode(encoding='UTF-8')
    
    print("Retrieving...")
    self.recordTime()    
    rangedList = self.rangeSearch(self.db1, keySt, keyEd)
    self.stopTime()
    
    if self.db1.get_type() == 2:
      rangedList.sort()
    print("Number of records retrieved within that range:", len(rangedList))
    
    text = list()
    
    for each in rangedList:
        key = each[0].decode(encoding='UTF-8')
        data = each[1].decode(encoding='UTF-8')

        text.append(key+"\n")
        text.append(data+"\n")
        text.append("\n")
        
    self.recordAnswer(text)
    self.answers.close()

    self.mainMenu()

  def recordTime(self):
    self.currentTime = datetime.now()

  """this just gets the current time now, and subtracts self.currentTime to get the total elapsed time. """
  def stopTime(self):
    stopTime = datetime.now()
    elapsedTime = stopTime - self.currentTime
    microsecs = elapsedTime.microseconds
    millisecs = microsecs * 1000

    print("The total time elapsed in microseconds was : %s" %(str(microsecs)))
    print("The total time elapsed in milliseconds was : %s" %(str(millisecs)))
    
  #Given textToWrite such as : textToWrite = ["a line of text", "another line of text", "a third line"]
  def recordAnswer(self,textToWrite):
    self.answers.writelines(textToWrite)

  #Prepare indexfile record answer
  def recordAnswerIndex(self,textToWrite):
   for i in textToWrite:
      self.answers.writelines(i[0].decode()+'\n')
      self.answers.writelines(i[1].decode()+'\n')
      self.answers.writelines('\n')

  #Do the equivalent of decode but on strings
  def cleanUpBinary(self,value):
    firstPivot = value.find("'")
    return value[firstPivot:]
  
  def destroyDB(self):
    self.db1.close()
    firstDBLocation = "./tmp/bpharris_db/"

    if self.DBType == 'indexfile':
      self.db2.close()
      secondDBLocation = "./tmp/bpharris_db/"

    if ((self.DBType == 'btree') or (self.DBType == 'hash')):
      os.system('rm -r '+str(firstDBLocation)+' -f')
      #self.db1.remove(firstDBLocation)
    
    if self.DBType == 'indexfile':
      os.system('rm -r '+str(firstDBLocation)+' -f')
      #os.system('rm -r '+str(secondDBLocation)+' -f')
      #self.db1.remove(firstDBLocation)
      #self.db2.remove(secondDBLocation)
    print("\nDatabases destroyed. Please re-create them or quit, \nor the program will become unstable.")

    self.mainMenu()

  """
  This program simply closes the cursor, truncates “answers” to nothing, removes the database folder, and then closes the program.
  """
  def quit(self):
    #self.answers.close()
    overWrite = open("answers","w")
    self.db1.close()
    firstDBLocation = "./tmp/bpharris_db/"

    if self.DBType == 'indexfile':
      self.db2.close()
      secondDBLocation = "./tmp/bpharris_db/indexfile"

    if ((self.DBType == 'btree') or (self.DBType == 'hash')):
      os.system('rm -r '+str(firstDBLocation)+' -f')
      #self.db1.remove(firstDBLocation)
    
    if self.DBType == 'indexfile':
      os.system('rm -r '+str(firstDBLocation)+' -f')
      #os.system('rm '+str(secondDBLocation)+' -f')
      #self.db1.remove(firstDBLocation)
      #self.db2.remove(secondDBLocation)
#self.destroyDB()
    sys.exit()

testData = P2Tests()

