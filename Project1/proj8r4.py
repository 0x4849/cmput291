#---------------------------------------------------------------
# Project:            1
# Due Date:             March 20th, 2014
# Name:                 Brad Harrison, Emmett Underhill, Ryan Satyabrata
# Lecture Section:      B1
# Instructor:           Li Yuan
# Lab Section:          Monday 1230 - 1400)
# Teaching Assistant:   Thorey
#---------------------------------------------------------------

import cx_Oracle
import getpass
import sys
import datetime

import random

class VehicleProject:
    #---------------------------------------------------------------
    # Function Name : __init__
    # Description: Sets up the connection to the oracle db, and
    # calls the main menu, which will be used to determine
    # which program the user wants to run.
    #
    # Important Variables: self.curs is used to execute statements
    # and self.con can be used to also interact with oracle. 
    #---------------------------------------------------------------
    
    def __init__(self):
        user = input("Username [%s]:" % getpass.getuser())
        if not user: 
            user=getpass.getuser()

        pw=getpass.getpass()

        conString=''+user+'/'+pw+'@gwynne.cs.ualberta.ca:1521/CRS'
        self.con = cx_Oracle.connect(conString)

        self.curs = self.con.cursor()
        self.commit = 'COMMIT'

    def mainmenu(self):
        print("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------")
        print("Welcome to the Application Program for the Auto Registration System.") 
        print("The following five application programs may be selected :")
        print("1 : New Vehicle Registration")
        print("    Information:\n    This program is used to register a new vehicle by an auto registration officer.")
        print("    For a previously unregistered vehicle, this program allows an officer to enter vehicle and personal information about its new owners.\n")
        print("2 : Auto Transaction")
        print("    Information:\n    This program is used to complete an auto transaction sale.\n    An officer can enter details about the seller, the buyer, the date, and the price of the sale.")
        print("\n3 : Driver Licence Registration")
        print("    Information:\n    This program is used to record the information needed to issue a driver licence including the personal info and a picture for the driver.")
        print("\n4 : Violation Record")
        print("    Information:\n    This program is used by a police officer to issue a traffic ticket and record the violation.")
        print("\n5 : Search Engine")
        print("    Information:\n    This program performs three different searches. \n    Search 5.1: Lists the name, licence number, address, birthday, driving  lass, driving condition, and the  	  expiring data of a driver. \n")
        print("    Search 5.2: Lists all violation records received by a person if the drive licence number or SIN is entered.\n")
        print("    Search 5.3: Lists the number of times that a vehicle has changed hands, the average price, and the number of violations it has been involved in.")
        print("\n    Alternatively press L to log out now.")
        print("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------")
        yourChoice = self.isMyChoice("Please enter your choice now. Possible choices are : 1, 2, 3, 4, 5.1, 5.2, 5.3, L\n")
        yourChoice = yourChoice.lower()
        while yourChoice != '1' and yourChoice != '2' and yourChoice != '3' and yourChoice != '4' and yourChoice != '5.1' and yourChoice != '5.2' and yourChoice != '5.3' \
        and yourChoice != 'l':
          print("Invalid choice.")
          yourChoice = self.isMyChoice("Please enter your choice now. Possible choices are : 1, 2, 3, 4, 5.1, 5.2, 5.3, L\n")
          yourChoice = yourChoice.lower()

        if yourChoice == '1':
            self.vehicleRegistration()
        
        elif yourChoice == '2':
            self.transaction()
        
        elif yourChoice == '3':
            self.driveLicenceRegistration()
        
        elif yourChoice == '4':
            self.violationRecords()
        
        elif yourChoice == '5.1':
            self.firstSearch()
        
        elif yourChoice == '5.2':
            self.secondSearch()

        elif yourChoice == '5.3':
            self.thirdSearch()


    #---------------------------------------------------------------
    # Function Name : driveLicenceInsert
    # Description: Inserts rows into the drive licence table
    # if the user has inputted an image filepath that does not
    # correspond to "null". This is a special function that works
    # with BLOB image types, and this function is able to insert
    # images into a table while using bind variables.
    #
    # Inputs: 
    # licence_no : The licence number inputted by user
    # sin : social insurance number inputted by user
    # dclass: driving class inputted by user
    # idate : list containing three list indices:
    # idate[0] : The year of the issuing date.
    # idate[1] : The month of the issuing date.
    # idate[2] : The day of the issuing date
    # edate : same as idate, but with licence expiring date.
    #---------------------------------------------------------------

    def driveLicenceInsert(self,licence_no,sin,dclass,idate,edate):
        photo = self.image
        self.curs.setinputsizes(photo=cx_Oracle.LONG_BINARY)
        insert = """insert into drive_licence (licence_no, sin, class, photo, issuing_date, expiring_date)
         values (:licence_no, :sin, :class, :photo, :issuing_date, :expiring_date)"""
        self.curs.execute(insert,{'licence_no':licence_no, 'sin':sin, 'class': dclass,  'photo':photo, 'issuing_date':datetime.date(idate[0],idate[1],idate[2]), 'expiring_date':datetime.date(edate[0],edate[1],edate[2])})
        self.curs.execute('COMMIT')


    #---------------------------------------------------------------
    # Function Name : myDateConversion
    # Description: Converts a string of "YYYY-MM-DD" into a list
    # containing [int(YYYY), int(MM), int(DD)]
    # This list is to be converted for use with datetime.date in order
    # to insert a date using a bind variable for the driveLicenceInsert
    # function.
    #
    # Input: A date given by the user in form of a string. 
    # Probably a driver's licence issuing date 
    # or a driver's licence expiring date.
    #
    # Output: list containing [int(YYYY), int(MM), int(DD)]
    # 
    # Example: "Input: Given string '1980-02-20', 
    # Returns a list [1980,02,20] in int format"
    #---------------------------------------------------------------

    
    def myDateConversion(self,string):
        firstPivot = string.find('-')
        year = string[:firstPivot]
        string = string[firstPivot+1:]
        nextPivot = string.find('-')
        month = string[:nextPivot]
        day = string[nextPivot+1:]
        
        return [int(year),int(month),int(day)]
    
    #---------------------------------------------------------------
    # Function Name : self.isDateTest(
    # Description: Given a date as a string, make sure that it's
    # in the properly handled 'YYYY-MM-DD' format. Else, keep asking
    # the user to re-input their date.
    #---------------------------------------------------------------
    
    def isDateTest(self, string):
      while True:
        if len(string) == 10 and string[0].isnumeric() and string[1].isnumeric() and \
        string[2].isnumeric() and string[3].isnumeric() and string[4] == '-' \
        and string[5].isnumeric() and string[6].isnumeric() and string[7] \
        == '-' and string[8].isnumeric() and string[9].isnumeric():
          return string
        else:
          print("\nInvalid date given. Please provide a new date.\n")
          string = input("\nProvide a date in 'YYYY-MM-DD' format such as \
          1980-10-02\n")

            
    #---------------------------------------------------------------
    # Function Name : isTooLong
    # Description: Given a string as inputted by the user,
    # and the question asked to obtain that input, and a maximum char
    # length, this function ensures that the user has not inputted
    # a string, which would violate the maximum char length as given
    # by the create table statements for the database.
    #
    # This helper function just makes sure that the maximum character  
    # length is being respected. If not, it keeps prompting the user 
    # to re-enter their input.
    #---------------------------------------------------------------
    
    def isTooLong(self, stringToInput, questionToAsk, maxCharLength):
        if len(stringToInput) <= maxCharLength:
          return stringToInput
        else:
          tooLong = True
          while (tooLong):
            print("\nThe values entered were too long. \nPlease enter a new value, and do not exceed the max length of :"+str(maxCharLength)+"\n")
            inputtedString = input(questionToAsk)
            tooLong = False
            if "," in inputtedString:
              inputtedString2 = inputtedString.split(",")
              for index in inputtedString2:
                if len(index) > maxCharLength:
                  tooLong = True
            else:
              if len(inputtedString) > maxCharLength:
                tooLong = True
          return inputtedString
          
    #---------------------------------------------------------------
    # Function Name : insertIntoSQL
    # Description: This function is given a table name and a list of
    # columns from colList, and it returns the correct Insert into Table
    # statement to be executed immediately by self.curs
    # 
    # The useful thing about this function is that you can pass in
    # integers or floating point numbers, and it will not put quotations
    # around these values. 
    # Also, if the value is a date type, then it will insert these properly
    # as well. Also, this function can insert null values correctly.
    # All other values will be inserted with quotations around them.
    # 
    # Input: A table name and a list of column values. 
    # The values must be in int or float type if they are to be added 
    # to SQL as integer or numeric.
    #
    # The keyword DATE must appear before any date in YYYY-MM-DD format.
    # i.e. 'DATE1980-10-02' is the correct input for that date.
    #
    # The column values must be in the correct order that 
    # they are to be inserted. 
    #
    # Output: An SQL insert statement containing all of the specified 
    # column names as well as the table name and any single quoted 
    # strings as needed.
    #
    # Example1: self.insertIntoSQL('owner',['1029304','1234567890','y']) 
    # Returns "Insert INTO owner VALUES('1029304','1234567890','y')
    #
    # Example2: self.insertIntoSQL('people',['s123456', 'Simon Cowell', 
    # 182, 80.22, 'BROWN','dark red', 
    # '12345-67 Ave. Edmonton AB T5P 497', 'm', 'DATE1976-05-28']
    #  Returns "Insert INTO people VALUES('s123456', 'Simon Cowell',
    # 182, 80.22, 'BROWN', 'dark red', '12345-67 Ave. Edmonton AB T5P 497'
    # ,'m', date '1976-05-28')
    #---------------------------------------------------------------

    def insertIntoSQL(self,table_name, colList):
      myStr = "INSERT INTO "+table_name+" VALUES("
      for index in colList:
        if type(index) == int or type(index) == float or index == 'null':
          myStr = myStr+str(index)+''','''
        elif 'DATE' in index:
          index2 = index.replace('DATE',"")
          index2 = 'date '+"'"+str(index2)+"',"
          myStr = myStr+index2
        else:
          myStr = myStr+"'"+str(index)+"',"
      myStr2 = myStr[:-1]
          
      myStr2 = myStr2+''')'''
      return myStr2
    
    
    #---------------------------------------------------------------
    # Function Name : ownerSinInsertion
    # Description: Given an owner sin value i.e. '129399394 y' is an
    # owner sin value where 'y' indicates that this person is the
    # primary owner of the vehicle. 
    # '12393993 n' is an owner sin value where 'n' indicates that this
    # person is the secondary owner of the vehicle.
    # And given a vehicle serial number, this function has a few
    # properties:
    #
    # 1) If the correct owner sin value was not given i.e. 'y'/'n'
    # do not appear in the value, then it keeps asking the user to
    # re-list it.
    # 2) If the owner sin value is too long i.e. greater than or equal
    # to 16 characters in length, then it will keep asking the uesr
    # to re-list it.
    # 3) If the user has entered an owner SIN that already belongs
    # to the vehicle, then it asks the user to re-enter the
    # owner sin value since this cannot be a legit new vehicle
    # registration.
    # 4) If the owner sin value is not in the people table, then
    # the user is asked whether he wants to add owner information
    # to both the people and the drive licence table, or to only
    # the people table.
    #
    # In either case of selecting the people or people/driver, the user
    # is prompted to add more personal information to insert this person
    # into the people table and possibly to the driver licence table.
    #
    # Input: A single owner SIN value and a vehicle serial number.
    # Output: The owner SIN will be added to the owner table, and
    # the owner information will also be added to the people/and or
    # the drive licence table if the user has specifeid this.
    #---------------------------------------------------------------

    def ownerSinInsertion(self,ownerSinValue,vehicleSN):
      ownerSinValue = ownerSinValue.lower()
      orig = ownerSinValue
      
      # Make sure that the sin value is only 15 characters + 2 characters for a space and a 'y' or 'n'
      if ' y' in ownerSinValue or ' n' in ownerSinValue: 
        ownerSinValue = self.isTooLong(ownerSinValue, "\nPlease provide a single owner SIN(no commas) followed by y or n to specify if someone is a primary owner or not. Example: 123456789 n \n", 17)
     
      # If the correct owner sin value was not given i.e. 'y'/'n'
      # do not appear in the value, then it keeps asking the user to
      # re-list it.
      needToCheckForNewSinLength = False
      while ' y' not in ownerSinValue and ' n' not in ownerSinValue:
        needToCheckForNewSinLength = True
        print("\nOne of your SINs has an invalid entry :"+str(ownerSinValue))
        ownerSinValue = input("\nInvalid format. Please provide an owner SIN followed by y or n to specify if someone is a primary owner or not. Example: 123456789 n \n")
      
      while ','  in ownerSinValue:
        print("\nPlease do not specify multiple entries again as they are already recorded and dealt with. Specify an individual entry here to replace the faulty entry here: \n"+str(orig))
        ownerSinValue = input()
      
      # Check if new sin value is less than or equal to 15 characters.
      if needToCheckForNewSinLength:
        ownerSinValue = self.isTooLong(ownerSinValue, "\nPlease provide a single owner SIN(no commas) followed by y or n to specify if someone is a primary owner or not. Example: 123456789 n \n", 17)
      
      if ' y' in ownerSinValue:
        firstPivot = ownerSinValue.find(' y')
        isPrimary = True
      else:
        isPrimary = False
        firstPivot = ownerSinValue.find(' n')

     
      actualSinValue = ownerSinValue[:firstPivot]
      actualSinValue = actualSinValue.replace(" ","")
      
      # Make sure that the actual sin value is not registered to this 
      # vehicle already.
      query = ("SELECT * FROM owner o where upper(o.owner_id) = upper('"+str(actualSinValue)+"') and upper(o.vehicle_id) = upper('"+str(vehicleSN)+"')")

      print("Executing query "+str(query))
      self.curs.execute(query)
      rows = self.curs.fetchall()
        
      if len(rows) >= 1:
        print("\nThis vehicle is already registered to this person. Please list a new owner SIN followed by y or n :\n")
        newOwnerID = input()
        self.ownerSinInsertion(newOwnerID, vehicleSN)
      
      # Check if the owner SIN is in the people table. If not, then 
      # prompt the user to add the owner SIN to people or people&drive
      # licence tables.
      newOwnerID = actualSinValue
      query = ("SELECT * FROM people p where upper(p.sin) = upper('"+str(actualSinValue)+"')")
      if len(rows) == 0:
        print("\nThis owner SIN, which is "+str(newOwnerID)+" is not currently in the database.\n Provide info for the person whose SIN is "+str(newOwnerID)+"\n")
        tableToAdd = self.isMyChoice("\nIf this person is a driver, then you can add this person's information to the driving license table. \nIf this person is not a driver, then you can add this person's info to only the people table. \nPress d to add to driver and people table. Press p to add only to people table. \n")
        while tableToAdd != 'd' and tableToAdd != 'p':
          print("\nInvalid selection. Please select d to add info to both drivers license table and people table. Press p to add info to only people table \n.")
          tableToAdd = input("\nIf this person is a driver, then you can add this person's information to the driving license table. \nIf this person is not a driver, then you can add this person's info to only the people table. \nPress d to add to driver and people table. Press p to add only to people table. \n")
        
        pname = self.isMyChoice("\nWhat is the person's name to add to the table? \n")
        # Make sure that the name is <= 40 characters in length.
        pname = self.isTooLong(pname, "\nWhat is the person's name to add to the table? \n",40)
        
        pheight = self.isMyChoice("\nWhat is the person's height to add to the table? \n")
        height = False
        while not height:
          try:
            height = True
            pheight = float(pheight)
          except:
            height = False
            print("\nInvalid input.\n")
            vtypeID = input("\nWhat is the person's height again?\n")
        
        pweight = self.isMyChoice("\nWhat is the person's weight to add to the table? \n")
        weight = False 
        while not weight:
          try:
            weight = True
            pweight = float(pweight)
          except(TypeError,ValueError):
            weight = False
            print("\nInvalid input.\n")
            pweight = self.isMyChoice("\nWhat is the person's weight again?\n")
        
        peyecolor = self.isMyChoice("\nWhat is the person's eye color to add to the table? \n")
        # Make sure eye color is <= 10 characters in length.
        peyecolor = self.isTooLong(peyecolor, "\nWhat is the person's eye color to add to the table? \n", 10)
        
        phaircolor = self.isMyChoice("\nWhat is the person's hair color to add to the table? \n")
        phaircolor = self.isTooLong(phaircolor, "\nWhat is the person's hair color to add to the table? \n", 10)
        
        paddr = self.isMyChoice("\nWhat is the person's address to add to the table? \n")
        paddr = self.isTooLong(paddr, "\nWhat is the person's address to add to the table? \n", 50)
        
        pgender = self.isMyChoice("\nWhat is the person's gender to add to the table? \nWrite m for male or f for female \n")
        while 'm' not in pgender and 'f' not in pgender:
            pgender=input("\nThis is an invalid gender option. Please specify m for male or f for female.\n")
        
        pbirthday = self.isMyChoice("\nWhat is the person's birthday to add to the table? \nWrite YYYY-MM-DD i.e. 1976-05-28\n")
        # Make sure that the date is a legit date in the correct format.
        pbirthday = self.isDateTest(pbirthday)
        pbirthday = 'DATE'+pbirthday
   
        insertionList = [newOwnerID,pname,pheight,pweight,peyecolor,phaircolor,paddr,pgender,pbirthday]
        SQLStatement = self.insertIntoSQL("people",insertionList)
        print("Executing SQL statement is "+str(SQLStatement))
        self.curs.execute(SQLStatement)
        
        if tableToAdd == 'd':
          license_no = self.isMyChoice("\nWhat is the license number of the person to add? \n")
          license_no = self.isTooLong(license_no, "\nWhat is the license number of the person to add? \n", 15)
          
          drivingClass = input("\nWhat is the driving class of the person to add? \n")
          drivingClass = self.isTooLong(drivingClass, "\nWhat is the driving class of the person to add? \n", 10)
          
          photo = self.isMyChoice("\nWhat is the fileName of the driver's photo to add?\n")
          
          if photo != "null" and photo != "NULL":
            imageFileURL = photo
            imageFound = False
            while not imageFound:
                try:
                    imageFound = True
                    f_image  = open(imageFileURL,'rb')
                    self.image = f_image.read()
                except:
                    imageFound = False
                    print("\nThis image file was not found on your hard drive. Please give a new file path.\n")
                    imageFileURL = self.isMyChoice("\nGive the new image file path now .\n")

          
          issuing_date = self.isMyChoice("\nWhat is the driver's issuing date of their license number? Write YYYY-MM-DD i.e. 1976-05-28\n")
          issuing_date = self.isDateTest(issuing_date)
          
          expiring_date = self.isMyChoice("\nWhat is the driver's expiring date of their license number? Write YYYY-MM-DD i.e. 1976-05-28\n")
          expiring_date = self.isDateTest(expiring_date)
   
          if photo != "null" and photo != "NULL":
              idate = self.myDateConversion(issuing_date)
              edate = self.myDateConversion(expiring_date)
              self.driveLicenceInsert(license_no, newOwnerID, drivingClass, idate, edate) 
              f_image.close()
          
          else:
            issuing_date = 'DATE'+issuing_date
            expiring_date = 'DATE'+expiring_date
            insertionList = [license_no, newOwnerID, drivingClass, photo, issuing_date, expiring_date]

            SQLStatement = self.insertIntoSQL("drive_licence", insertionList)
            print("Executing SQL statement is "+str(SQLStatement))
            self.curs.execute(SQLStatement)
      

      if isPrimary:
        insertionList =  [newOwnerID, vehicleSN, 'y']
      else:
        insertionList = [newOwnerID, vehicleSN, 'n']
      
      # Now that people/drive_licence table have been handled, it's
      # now okay to add to owner table without violating foreign key
      # constraints.
      SQLStatement = self.insertIntoSQL("owner",insertionList)
      print("Executing SQL statement is "+str(SQLStatement))
      self.curs.execute(SQLStatement)
      
    #---------------------------------------------------------------
    # Function Name : vehicleRegistration
    # Description: After prompting the user to enter new vehicle 
    # information such as serial number, maker, model, etc, it will add
    # the vehicle to the vehicle table provided that the vehicle 
    # serial number does not exist in the vehicle table. 
    # Also, by calling ownerSinInsertion,
    # it will add the owner information to the owner table and possibly
    # to both people and people/drive_licence if the information does
    # not exist there and the user indicates that they want to add it
    #---------------------------------------------------------------      
  
    def vehicleRegistration(self):
      serial_no = self.isMyChoice("What is the serial_no of the new vehicle you wish to register?")
      
      query = ("SELECT * FROM vehicle v where upper(v.serial_no) = upper('"+str(serial_no)+"')")
      print("Executing query "+str(query))
      self.curs.execute(query)
      rows = self.curs.fetchall()
      
      while len(rows) >= 1:
          serial_no = self.isMyChoice("\nThis vehicle serial number already exists in the database. Please enter a valid serial number for a new vehicle. Or press q to return to main menu.\n")
          if serial_no == 'q':
            #self.mainMenu()
            break
          else:
            query = ("SELECT * FROM vehicle v where upper(v.serial_no) = upper('"+str(vehicleSN)+"')")
            print("Executing query "+str(query))
            self.curs.execute(query)
            rows = self.curs.fetchall()
            
      vmaker = self.isMyChoice("\nWhat is the vehicle maker name?\n")
      vmaker = self.isTooLong(vmaker, "\nWhat is the vehicle maker name?\n", 20)
      
      vmodel = self.isMyChoice("\nWhat is the vehicle model name?\n")
      vmodel = self.isTooLong(vmodel, "\nWhat is the vehicle model name?\n", 20)
      
      vyear = self.isMyChoice("\nWhat is the vehicle manufacturating year?\n")
      
      vcolor = self.isMyChoice("\nWhat is the vehicle's colour?\n")
      vcolor = self.isTooLong(vcolor, "What is the vehicle's colour?", 10)
      
      '''print("\nCurrently the type IDs to choose from are : 1 for Subcompact car, 2 for Compact car, 3 for Intermediate car, 4 for Full-Size vehicle, 5 for Compact Pickup,\n6 for full-size pickup, 7 for Compact utility, 8 for Intermediate Utility, 9 for Full-size Utility, 10 for Mini-Van, and 11 for Full-Size Van\n") 
      '''      
        
      query = "SELECT * FROM vehicle_type vt GROUP By vt.type_id, vt.type"
      self.curs.execute(query)
      rows =self.curs.fetchall()
      typeIDs = [str(row[0]) for row in rows]
      try:
        vTypes = [row[1].strip() for row in rows]
      except:
        vTypes = [row[1] for row in rows]

      print("\nThe choices for vehicle types iclude :")
      for i in range(len(typeIDs)):
        print("\n Vehicle Type : "+str(vTypes[i])+" which has a type id of : "+str(typeIDs[i]))
#print(rows)
        
      vtypeID = self.isMyChoice("Please enter the type ID of the vehicle:\n  (Valid types are: %s)\n" %(typeIDs))

      while vtypeID not in typeIDs :
        vtypeID = self.isMyChoice("Please enter a valid type ID of vehicle:\n  (Valid types are: %s)\n" %(typeIDs))

      typeId = False
      while not typeId:
        try:
          typeId = True
          vtypeId = int(vtypeID)
        except(TypeError,ValueError):
          typeId = False
          print("\nInvalid input.\n")
          vtypeID = self.isMyChoice("\nWhat is the vehicle's typeID?\n")
        
      year = False
      while not year:
        try:
          year = True
          vyear = int(vyear)
        except(TypeError,ValueError):
          year = False
          print("\nInvalid input.\n")
          vyear = self.isMyChoice("\nWhat is the vehicle's manufacturing year?\n")
      
      vList = [serial_no,vmaker,vmodel,vyear,vcolor,vtypeId]
      SQLStatement = self.insertIntoSQL("vehicle",vList)
      
      print(SQLStatement)
      self.curs.execute(SQLStatement)
        
      ownerSIN = self.isMyChoice("\nGive the vehicle owner SINs and use a space then y or n to specify if they are the primary owner. \nUse commas(without spaces after the comma) to specify multiple owners as needed. \nExample: 123456789 y,123456781 n \n")

      if ',' in ownerSIN:
        myList = ownerSIN.split(',')
        for index in myList:
          self.ownerSinInsertion(index, serial_no)
      else:
          self.ownerSinInsertion(ownerSIN, serial_no)

      commitChange = input("\nChanges done to database. Do you wish to commit them? Enter y for yes.\n")
      if commitChange:      
        self.curs.execute(self.commit)
      self.mainmenu()
  
  
    #---------------------------------------------------------------
    # Function Name : transaction
    # Description: This program will prompt for a vehicle serial number
    # to the user along with a list of buyer SINs and if they are primary
    # owners or not. It will also ask for other auto_sale information, 
    # but the transaction will only be recorded under the primary buyer
    # and the primary seller.
    # This is because we cannot  have multiple duplicate transaction IDs.
    #
    # However, the sellers will all lose their ownership information 
    # from the owner table, and additionally, all of the owners will be 
    # added to the owner table. 
    # If the buyer SIN is not in the people table, 
    # then by way of calling ownerSinInsertion, the user will be
    #  prompted to add them to both the people table and the 
    # drive licence table or only to the people table
    #---------------------------------------------------------------      

  
    def transaction(self):
      vehicleSN = self.isMyChoice("What is the vehicle serial number of the vehicle being sold? \n")
      findPrimarySellerQuery = "SELECT owner_id FROM owner o where upper(vehicle_id) = upper('"+str(vehicleSN)+"') and is_primary_owner = 'y'"
      self.curs.execute(findPrimarySellerQuery)
      rows = self.curs.fetchall()

      while len(rows) == 0:
          print("\nThis vehicle was not found in the database. Please re-specify the vehicle ID.\n")
          vehicleSN = self.isMyChoice("\nWhat is the vehicle serial number of the vehicle being sold? \n")

          findPrimarySellerQuery = "SELECT owner_id FROM owner o where upper(vehicle_id) = upper('"+str(vehicleSN)+"') and is_primary_owner = 'y'"
          self.curs.execute(findPrimarySellerQuery)
          rows = self.curs.fetchall()
      rows = [row[0] for row in rows]
      primarySeller = rows[0]
      primarySeller = primarySeller.strip()
      
      ownerSIN = self.isMyChoice("\nGive a list of buyer SINs along with if they are primary owners or not. Example: 12345679 y or 123486970 n .Separate a multiple buyer list with commas as needed: 1234 y, 1293 n\n")

      saleDate = self.isMyChoice("\nWhat is the transaction sale date ? \nWrite YYYY-MM-DD i.e. 1976-05-28 \n")
      saleDate = self.isDateTest(saleDate)
      
      price = self.isMyChoice("\nWhat is the price of the auto sale? \n")
      sellerList = self.isMyChoice("\nWhat is the list of seller SINs followed by commas? i.e. 123456, 123494 \n")
      sellerList = sellerList.split()
      while primarySeller not in sellerList:
          print("\nThe primary owner of this vehicle "+str(primarySeller)+" was not listed in your seller SIN list. A non-primary owner cannot sell a vehicle.\nPlease re-enter your seller SINs as needed.\n")
          sellerList = input("\nWhat is the list of seller SINs followed by commas? i.e. 123456, 123494 \n")
          sellerList = sellerList.split()
    
      transactionID = self.randomGen("transaction", "transaction_id",10)
      thePrice = False
      while not thePrice:
        try:
          thePrice = True
          price = float(price)
        except(TypeError, ValueError):
          thePrice = False
          print("\nInvalid input. for price\n")
          price = self.isMyChoice("\nWhat is the price of the auto sale?\n")
              
      saleDate = 'DATE'+saleDate
      

      deleteQuery = "delete from owner where vehicle_id = '"+str(vehicleSN)+"'"
      print("Executing query "+str(deleteQuery))
      self.curs.execute(deleteQuery)
      
      if ',' in ownerSIN:
        #Split the owner sins up into a list separated by the commas
        myList = ownerSIN.split(',')
        for index in myList:
          #For each owner sin value, insert it...
          self.ownerSinInsertion(index, vehicleSN)

          # if it's a primary owner, then this SIN will be used to
          # identify the primary buyer for the transaction.
          if ' y' in index:
            pivot = index.find(' y')
            theIndex = index[:pivot]
            theIndex = theIndex.replace(" ","")
            
      else:
        self.ownerSinInsertion(ownerSIN, vehicleSN)
          # if it's a primary owner, then this SIN will be used to
          # identify the primary buyer for the transaction.
        if ' y' in ownerSIN:
          pivot = ownerSIN.find(' y')
          theIndex = ownerSIN[:pivot]
          theIndex = theIndex.replace(" ","")
              
      primaryBuyer = theIndex
      theQueryIndices = [transactionID, str(primarySeller), str(primaryBuyer), vehicleSN, saleDate, price]
      SQLStatement = self.insertIntoSQL("auto_sale",theQueryIndices)
      print("Executing query "+str(SQLStatement))
      self.curs.execute(SQLStatement)


      commitChange = input("\nChanges done to database. Do you wish to commit them? Enter y for yes.\n")
      if commitChange:      
        self.curs.execute(self.commit)
     
      self.mainmenu()
    
    #---------------------------------------------------------------       
    #Function Name : randomGen
    #Description: Generates random number whoese first digit is always 1
    #Parameters are the target table name, the target column name and how many digits you want.
    #---------------------------------------------------------------      
    
    def randomGen(self, tableName, columnName, digits=9):
        while(True):
            rangen = random.SystemRandom()
            ranNo = round((rangen.random()+1)*10**(digits-1))
            
            #Check if ticket_no exists, and if so it will get another random number.
            query = ("SELECT * FROM %s a where a.%s = %s" %(tableName, columnName, ranNo))
            self.curs.execute(query)
            rows = self.curs.fetchall()
            
            if len(rows) == 0:
                #print("Unique_No %d" %(ranNo))
                return ranNo   
    
    #---------------------------------------------------------------      
    #Function Name : violationRecords
    #Description: Violation Records, this component is used by a police officer to issue a traffic ticket and record the violation.
    #---------------------------------------------------------------      

        
    def violationRecords(self):
        ticketNo = self.randomGen("ticket", "ticket_no",9)
        
        while(True):
            violatorNo = self.isMyChoice("Please enter the violator's SIN:\n")
            
            query = ("SELECT * FROM people a where upper(a.sin) = upper('%s')" %(violatorNo))

            self.curs.execute(query)
            rows = self.curs.fetchall()
                
            if len(rows) != 0:
                break
            else:
                print("Error - Entry does not exist!\n")
                
        while(True):
            vehicleNo = self.isMyChoice("Please enter the violator vehicle's serial number:\n")
            
            query = ("SELECT * FROM vehicle a where upper(a.serial_no) = upper('%s')" %(vehicleNo))
            self.curs.execute(query)
            rows = self.curs.fetchall()
                
            if len(rows) != 0:
                break
            else:
                print("Error - Invalid vehicle serial number!\n")
        
        while(True):
            officeNo = self.isMyChoice("Please enter officer's SIN:\n")
            
            query = ("SELECT * FROM people a where upper(a.sin) = upper('%s')" %(officeNo))
            self.curs.execute(query)
            rows = self.curs.fetchall()
                
            if len(rows) != 0:
                break
            else:
                print("Error - Entry does not exist!\n")
                
        
        query = ("SELECT * FROM ticket_type tt")
        self.curs.execute(query)
        row = self.curs.fetchall()
        
        vtypeList = []        
        for each in row:
            vtypeList.append(each[0].lower().strip(' '))
        vTypes = ", ".join(vtypeList)
        
        vtype = self.isMyChoice("Please enter the type of violation:\n  (Valid types are: %s)\n" %(vTypes)).lower()
        while vtype not in vtypeList:
            vtype = self.isMyChoice("Please enter a valid type of violation:\n  (Valid types are: %s)\n" %(vTypes)).lower()
        
        vdate = self.isMyChoice("Please enter date of violation in YYYY-MM-DD format:\n")
        vdate = self.isDateTest(vdate)
        vdate = "DATE"+vdate
        
        place = self.isMyChoice("Please enter the place of violation (Max. 20 characters):\n")
        place = self.isTooLong(place, "Please enter the place of violation (Max. 20 characters):\n",20)
        
        descriptions = self.isMyChoice("Please enter the description for the violation (Max. 1024 characters):\n")
        descriptions = self.isTooLong(descriptions,"Please enter the description for the violation (Max. 1024 characters):\n", 1024)
        
        newTicket = [ticketNo, violatorNo,vehicleNo,officeNo,vtype,vdate,place,descriptions]
        query = self.insertIntoSQL('TICKET', newTicket)
        self.curs.execute(query)
        
        self.curs.execute(self.commit)
        
        self.mainmenu()
        

    def isMyChoice(self,myInput):
        isMyChoice = False
        while not isMyChoice:
            theInputValue = input(myInput)
            theInputValue = theInputValue.replace("'","")
            isCorrectChoice = input("Press enter to continue or 'b' to go back and re-enter. \n")
            isCorrectChoice = isCorrectChoice.lower()
            if isCorrectChoice != 'b' and isCorrectChoice != 'back':
                isMyChoice = True
                
        return theInputValue


    #---------------------------------------------------------------      
    #Function Name : secondSearch
    #Description: Search the violation Records, it lists all violation records 
    #received by a person if the drive licence_no or sin of a person  is entered.
    #---------------------------------------------------------------      


    def secondSearch(self):
        #LNUM124 or s123450
        sinOrLic = self.isMyChoice("Please enter SIN or Driver Licence Number:\n").upper()

        query = ("""SELECT t.ticket_no AS "TICKET ID", t.VEHICLE_ID AS "VEHICLE ID",
                t.OFFICE_NO AS "OFFICER", t.VDATE AS "DATE", t.PLACE, t.VTYPE AS "TYPE", 
                t.DESCRIPTIONS FROM ticket t, drive_licence d, people p 
            WHERE (t.violator_no = p.sin AND upper(p.sin) = upper('%s')) 
                OR (upper(d.licence_no) = upper('%s') AND t.violator_no = d.sin) 
            GROUP BY t.ticket_no, t.VEHICLE_ID, t.OFFICE_NO, t.VDATE, t.PLACE, t.VTYPE, t.DESCRIPTIONS"""
            % (sinOrLic, sinOrLic))
        self.curs.execute(query)
        
        rows = self.curs.fetchall()
        colName = self.curs.description
        colText = ""
        rowsText = ""
        
        i=0
        while(i<len(colName)):
            if i+1 != len(colName):
                colText += str(colName[i][0]).ljust(colName[i][2]) + " "
            else:
                colText += str(colName[i][0]).strip()
            i+=1

        for each in rows:
            i=0
            for item in each:
                if i+1 != len(each):
                    rowsText += str(item).ljust(colName[i][2]) + " "
                else:
                    rowsText += str(item).strip(" ") + " "
                i+=1
            rowsText+="\n"

        print("%s\n%s"%(colText, rowsText))        
        self.mainmenu()  
        
    def thirdSearch(self):
      #search 3 start
      vehicleSN = self.isMyChoice(" What is the vehicle serial number to be searched \n")
      
      query = ("SELECT * FROM vehicle v where upper(v.serial_no) = upper('"+str(vehicleSN)+"')")
      self.curs.execute(query)
      rows = self.curs.fetchall()
      while len(rows) == 0:
          print("\n This serial number was not found as a registered. vehicle. Please re-enter a valid entry. \n")
          vehicleSN = input("\nWhat is the vehicle serial number to be searched \n")
          query = ("SELECT * FROM vehicle v where upper(v.serial_no) = upper('"+str(vehicleSN)+"')")

          self.curs.execute(query)
          rows = self.curs.fetchall()
      

          
      #Number of times vehicle has changed hands:
      query = ("select count(*) from auto_sale a where upper(a.vehicle_id) = upper('"+str(vehicleSN)+"')")
      
      self.curs.execute(query)
      rows = self.curs.fetchall()
      rows = [row[0] for row in rows]
      numberChanged = rows[0]
      #numberChanged2 = numberChanged.strip()
      #Average Price:
      query2 = ("select avg(a.price) from auto_sale a where a.vehicle_id = '"+str(vehicleSN)+"'")
      self.curs.execute(query2)
      rows = self.curs.fetchall()
      rows = [row[0] for row in rows]
      averagePrice = rows[0]

      #Number of Violations vehicle has been involved in:
      query3 = ("select count(*) from ticket t where t.vehicle_id = '"+str(vehicleSN)+"'")
      self.curs.execute(query3)
      rows = self.curs.fetchall()
      rows = [row[0] for row in rows]
      numberViolations = rows[0]

      print("\n The number of times to vehicle has changed hands is :\n "+str(numberChanged)+"\n")
      if str(averagePrice) == 'None':
          print("\n This vehicle has never changed hands, so there is no average price of it during sales.")

      else:
          print("\n The average price of the vehicle during the times it changed hands is:\n $"+str(averagePrice)+"\n")
      print("\n The number of times this vehicle has been involved in a violation is:\n "+str(numberViolations)+"\n")

      #Case insensitive search:
      #select * from people p where upper(p.name) = upper('frank darabont');
      self.mainmenu() 

    #--------------------------------------------------------------- 
    # Function Name : dirveLicenceRegistration
    # Description: Allows user to regiser driver's licence information.
    # User is asked for a unique licence_no, and reprompted until a 
    # unique value is entered. User is also prompted for a currently
    # existing SIN, and reprompted until one is entered. Requests
    # a licence class, filename of licence photo, issue date and 
    # expiry date. All of this data is then inserted into the SQL table. 
    #---------------------------------------------------------------
    def driveLicenceRegistration(self):
      licence_no = input("\nWhat is the license number of the person to add? \n")
     # license_no = self.isTooLong(license_no, "\nWhat is the license number of the person to add? \n", 15)
      query = ("SELECT * FROM drive_licence l WHERE upper(l.licence_no) = upper('"+str(licence_no)+"')")
      self.curs.execute(query)
      rows = self.curs.fetchall()
      while len(rows) >= 1:
        license_no = input("\nThe input you have entered already exists in the database, please insert a unique licence_no \n")
        license_no = self.isTooLong(license_no, "\nThe input you have entered already exists in the database, please insert a unique licence_no \n", 15)
  
        if licence_no == 'q':
          break 
        else:
          query = ("SELECT * FROM drive_licence l WHERE upper(l.licence_no) = upper('"+str(licence_no)+"')")
          self.curs.execute(query)
          rows = self.curs.fetchall()
      dsin = input("\nWhat is the SIN of the licence holder?\n")
      dsin = self.isTooLong(dsin, "\nWhat is the SIN of the licence holder?\n", 17) 
      query = ("SELECT * FROM drive_licence l WHERE upper(l.sin) = upper('"+str(dsin)+"')")
      self.curs.execute(query)
      rows = self.curs.fetchall()
      while len(rows) < 1:
        dsin = input("\nThis SIN does not exist in the data base, please enter a valid SIN, or add this SIN to the database before continueing.\n")
        dsin = self.isTooLong(dsin,"\nThis SIN does not exist in the data base, please enter a valid SIN, or add this SIN to the database before continueing.\n",17)
        if dsin == 'q':
          break
        else:
          query = ("SELECT * FROM drive_licence l WHERE upper(l.sin) = upper('"+str(dsin)+"')")
          self.curs.execute(query)
          rows = self.curs.fetchall()

      drivingClass = input("\nWhat is the driving class of the person to add? \n")
      drivingClass = self.isTooLong(drivingClass, "\nWhat is the driving class of the person to add? \n", 10)
          
      photo = input("\nWhat is the fileName of the driver's photo to add?\n")
          
      if photo != "null" and photo != "NULL":
        imageFileURL = photo
        imageFound = False
        while not imageFound:
          try:
            imageFound = True
            f_image  = open(imageFileURL,'rb')
            self.image = f_image.read()
          except:
            imageFound = False
            print("\nThis image file was not found on your hard drive. Please give a new file path.\n")
            imageFileURL = input("\nGive the new image file path now .\n")

          
      issuing_date = input("\nWhat is the driver's issuing date of their license number? Write YYYY-MM-DD i.e. 1976-05-28\n")
      issuing_date = self.isDateTest(issuing_date)
          
      expiring_date = input("\nWhat is the driver's expiring date of their license number? Write YYYY-MM-DD i.e. 1976-05-28\n")
      expiring_date = self.isDateTest(expiring_date)
   
      if photo != "null" and photo != "NULL":
        idate = self.myDateConversion(issuing_date)
        edate = self.myDateConversion(expiring_date)
        self.driveLicenceInsert(license_no, newOwnerID, drivingClass, idate, edate) 
        f_image.close()
          
      else:
        issuing_date = 'DATE'+issuing_date
        expiring_date = 'DATE'+expiring_date
        insertionList = [license_no, dsin, drivingClass, photo, issuing_date, expiring_date]

      SQLStatement = self.insertIntoSQL("drive_licence", insertionList)
      print("Executing SQL statement is "+str(SQLStatement))
      self.curs.execute(SQLStatement)
  
      commitChange = input("Changes done to database. Do you wish to commit them? Enter y for yes.\n")
      if commitChange:      
        self.curs.execute(self.commit)
      self.mainmenu()

vuser = VehicleProject()
#vuser.search_engine()
vuser.mainmenu()
#vuser.transaction()
