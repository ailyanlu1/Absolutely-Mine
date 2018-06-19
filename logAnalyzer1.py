#/usr/bin/env python

import os
import re
from datetime import datetime
import time

msgList = ["INFO","WARNING","ERROR","DEBUG","ALARM"]
logFiles = []
fulltechFiles = []
currentDate = time.strftime("%d-%m-%Y")       					#Fetching the current date
flag = 0


def showOutput():
	try:
		if flag == 3:
			fHandleRead = open("timelog" + currentDate + ".txt","r")
		elif flag == 2:
			fHandleRead = open("PatternLogs" + currentDate + ".txt","r")
		elif flag == 1:
			fHandleRead = open("allLogs" + currentDate + ".txt","r")
		
		for line in fHandleRead.readlines():
			print (line)
	finally:
		fHandleRead.close()

		
def formatTime(unformattedTime):							#formatting function
        unformattedTime = ''.join(e for e in unformattedTime if e.isalnum())
	year = unformattedTime[4:6]
        month = unformattedTime[0:2]
        day = unformattedTime[2:4]
        time = unformattedTime[6:]
        formattedTime = year+month+day+time

        return int(formattedTime)

def formatDecodedTime(unformattedTime):							#formatting function for decoded file
	unformattedTime = ''.join(e for e in unformattedTime if e.isalnum())
	year = unformattedTime[2:4]
	month = unformattedTime[4:6]
	day = unformattedTime[6:8]
	time = unformattedTime[8:]

	formattedTime = year+month+day+time

	return int(formattedTime)

def timeBasedLog(startTime,endTime):
	
	global flag
	
	startTime=formatTime(startTime)
	endTime=formatTime(endTime)
	
	if flag ==2 :
		fHandleRead = open("PatternLogs" + currentDate + ".txt","r")
	else:
		fHandleRead = open("allLogs" + currentDate + ".txt","r")
	
	fHandleWrite = open("timelog" + currentDate + ".txt","w")

	for line in fHandleRead.readlines():

		line = line.rstrip('\n').rstrip('\r')
		match = re.search(r'^[(\*)|(\s+Logfile)|(\-)]',line)
		if match:
			
			fHandleWrite.write(line+"\n")
			continue
		

		tempTime = re.match(r'[\w\W]+\s+\[([\w\W]{21})\].*',line)
	
		decodedTempTime = re.match(r'^([\w\W]{23}).*',line)		
		
		if tempTime:
		      	tempTime = tempTime.group(1)
		      	time = tempTime[:-7]
			time = formatTime(time)
			if(time >= startTime and time <= endTime):
				fHandleWrite.write(line+"\n")
		else:
			if decodedTempTime:
				decodedTempTime = decodedTempTime.group(1)
				time = decodedTempTime[:-7]
				time = formatDecodedTime(time)

				if (time >=startTime and time <= endTime):
					fHandleWrite.write(line+"\n")
	
	fHandleWrite.close()				
	flag = 3

def patternBasedLogAND(searchString):
	global flag
        flag =2

        fHandleWrite = open("PatternLogs" + currentDate + ".txt","w")
	fHandleRead = open("allLogs" + currentDate + ".txt","r")

	header = "\n\n----------------------------------------------------------------------------- \n\t "
	
	for i in searchString:
		header += "      "+ i + "   &"
	header = header[:-1]
	header += "\n------------------------------------------------------------------------------- \n\n "

	fHandleWrite.write(header)

	for line in fHandleRead.readlines():
		countSearch = 0
		if re.search(r'^\*+$',line) or re.search(r'^\s+Logfile*',line):
			fHandleWrite.write(line)
			continue

		for item in searchString:
			if re.search(item,line):
				countSearch+=1

		if countSearch == len(searchString):
			fHandleWrite.write(line)

	fHandleWrite.close()
	fHandleRead.close()		
				
	
def patternBasedLogOR(searchString):

	global flag
	flag =2 
        fHandleWrite = open("PatternLogs" + currentDate + ".txt","w")	
		
	

	for item in searchString:
		header = "\n\n------------------------  "+item+"  ----------------------------------\n\n"
		
		fHandleWrite.write(header)

		fHandleRead = open("allLogs" + currentDate + ".txt","r")
		
		for line in fHandleRead.readlines():
			line = line.rstrip('\n').rstrip('\r')

			match = re.search(item,line)
			if match:
				fHandleWrite.write(line+"\n")
				continue

			match = re.search(r'^[(\*)|(\s+Logfile)]',line)
			if match:
                                fHandleWrite.write(line+"\n")
		fHandleRead.close()		
	fHandleWrite.close()

def segregatedFullLog(fileTypeChoice):
	global flag
	flag =1
	#To remove all data from previous execution
	if (os.path.isfile("allLogs" + currentDate + ".txt")):
		fh = open("allLogs" + currentDate + ".txt","w")
		fh.close()
		
	for file in logFiles:

		infoList = []							#list of info messages
		warningList = []						#list of warning messages
		errorList =[]							#list of error messages
		debugList =[]							#list of debug messages
		alarmList =[]							#list of alarm messages

		fullList = []							#list of all messages
		
		listOfMsgList = [infoList,warningList,errorList,debugList,alarmList]		#list of all the message list
		
		fHandleRead = open(file,"r")				#opening Log file of VSP-9k in read mode
		
		baseMac =""	
		if(fileTypeChoice == '1'):
			for line in fHandleRead.readlines():
				line = line.rstrip('\n').rstrip('\r')
				
				match = re.search(r'(<NP>.*</NP>)\s([\w\W]*)',line)
	
				if match:
					fullList.append(match.group(2))
				else:
					decodeMatch = re.match(r'^\d{4}.*',line)
					if decodeMatch:
						fullList.append(line)	     
			fHandleRead.close()

		elif (fileTypeChoice == '2'):
			check = 0
                	for line in fHandleRead.readlines():
                	        line = line.rstrip('\n').rstrip('\r')
	
	                        match = re.search(r'^Command[\w\W]+\[\sshow logging file\s\]',line)
				
				if re.search(r'^\s+BaseMacAddr',line):
					baseMac = line
					
				
	                        if match:
	                                check = 1
	                                continue
	
	                        match2 = re.search(r'^Command',line)
	                        if (match2 and check==1):
	                                check = 2
	
	                        if (check==1):
	                                if re.search(r'^[\w]+',line):
	                                        fullList.append(line)
	                                continue
	
	                fHandleRead.close()


		# Start Segregating the messages of each file

		for item in fullList:
			if re.search(r'INFO',item):
				infoList.append(item)

			elif (re.search(r'WARNING',item)):
				warningList.append(item)

			elif (re.search(r'ERROR',item)):
				errorList.append(item)

			elif (re.search(r'DEBUG',item)):
				debugList.append(item)

			elif (re.search(r'ALARM',item)):
				alarmList.append(item)

		
		headerTag = "\n\n*****************************************************************************"
		headerTag+="\n				Logfile Name: " + file
		if (fileTypeChoice == '2'):
			headerTag+="\n			"+baseMac
		headerTag+="\n*****************************************************************************\n\n\n"
		


		#To check if the file to be written on already exists or not. If not, create a new file, else append to it.
		
		if (os.path.isfile("allLogs" + currentDate + ".txt")):
			fHandleWrite = open("allLogs" + currentDate + ".txt","a")
		else:
			fHandleWrite = open("allLogs" + currentDate + ".txt","w")
		
		fHandleWrite.write(headerTag)
		
		countMsg = 0
		for itemList in listOfMsgList:
			if itemList:
				seperator = "\n########################################################################"
				seperator+= "\n-------------------"+msgList[countMsg]+"------------------------------"
				seperator+= "\n#######################################################################"
					
				#print (seperator)
				countMsg+=1
				fHandleWrite.write(seperator+"\n")
				for item in itemList:
					#print (item)
					fHandleWrite.write(item+"\n")
				#print ("\n")
				fHandleWrite.write("\n")
		fHandleWrite.close()
			
def userInput() :

	global logFiles
	global msgList	
	#countLogFiles = 0
	#countFulltechFiles = 0
	searchString = []
	while(1):
		countLogFiles = 0
		print("\n\nDo you want to search from\n\n	1.logfiles\n	2.show fulltech file\n")
		fileTypeChoice = raw_input("Enter your choice(1 or 2):")
		if (fileTypeChoice == '1'):
			while(1):
				logChoice = raw_input("\nDo you want to search from:\n\n	1.File\n	2.Folder\n\nEnter your Choice(1 or 2):")
				if(logChoice=='1'):
					userLogFiles = (raw_input("\nEnter the logfiles (seperated by ',')(max 10) : "))
					userLogFiles = userLogFiles.split(",")
				
					for file in userLogFiles:
						if not(os.path.isfile(file)):
							print (file +" not present")
						else:
							logFiles.append(file)
							countLogFiles += 1
		
				elif(logChoice=='2'):
					logPath = raw_input("\nPlease enter path of folder : ")
					if(not(os.path.isdir(logPath))):
						print("\nThere is no directory at the given path")
						continue

					for files in os.listdir(logPath):
						if(re.search(r'^log\.[\w]+.\d{3}$',files)):
							logFiles.append(files)
							countLogFiles += 1 
						elif (re.search(r'^log\.[\w]+.\d{3}.txt$',files)):
							logFiles.append(files)
                                                        countLogFiles += 1

					if(countLogFiles>0 and countLogFiles<11):
						print ("\nThe logfiles in the given folder are:\n")
						for files in logFiles:
							print ("\t"+files)

				else:
					print("\nWrong choice entered\n")
					continue
		
				if countLogFiles == 0:
					print ("\nSorry! No logfiles are present")
		
				elif (countLogFiles>10):
					print ("\nSorry! More than 10 logfiles")
				
				else:
					break
			
			segregatedFullLog(fileTypeChoice)  #Call to segregate the logs of all logfilesf
			break

		elif (fileTypeChoice == '2'):
			countFulltechFiles=0
			while(1):
				fulltechFilesInput = raw_input("\nEnter show fulltech file names (seperated by ',') : ")
				fulltechFilesInput = fulltechFilesInput.split(",")

				for file in fulltechFilesInput:
							if not(os.path.isfile(file)):
								print (file +" not present")
							else:
								logFiles.append(file)
								countFulltechFiles += 1	
					
				if (countFulltechFiles == 0):
					print ("No files present")
				else:
					break

			segregatedFullLog(fileTypeChoice)
			break
				
		else:
			print ("\nWrong choice entered")
			continue

	print("\n\n")

	check = raw_input("Do you want a pattern search  (y/n) : ")

	if check in ['y','Y']:
		while(1):
			print("\n\nWhat kind of search do you prefer?\n")
			print("	1.All words should be present in a single line (AND)\n")
			print("	2.Normal pattern search (OR) \n")
			patternChoice = raw_input("Enter your Choice(1 or 2):")
	
			if(patternChoice == '1'):				
				userSearchString = raw_input("\nEnter the strings (seperated by ',') : ")

				searchString = userSearchString.split(",")

				for item in userSearchString:
	                        	if (re.search(r'^\s+$',userSearchString)):
	                                	print ("Invalid Input")
	                                        continue
				break
	
			elif(patternChoice == '2'):
				print ("\n	Message level search (INFO,WARNING,DEBUG,ERROR,ALARM)\n		OR\n	 Pattern search\n")
	
				userSearchString = raw_input("\nEnter the strings (seperated by ',') : ")
					
				userSearchString = userSearchString.split(",")
			
				for item in userSearchString:
					if (re.search(r'^\s+$',item)):
	                                       	print ("Invalid Input\nPlease Re-enter")
	                                        continue
	
				for item in userSearchString:
					if item.upper() in msgList:
						searchString.append(item.upper())
					else:
						searchString.append(item)
				break
			else:
				print ("\nWrong choice entered\nPlease re-enter")
				continue
		
		if(patternChoice == '1'):	
			patternBasedLogAND(searchString)	
		elif(patternChoice == '2'):
			patternBasedLogOR(searchString)
			

	check = raw_input("\n\nDo you want to enter time range (y/n) : ")
  	if check in ['y','Y']:
		while (1):
			startTime = raw_input("Enter the starting date and time in (mm/dd/yy hh:mm) : ")
			endTime = raw_input("Enter the end date and time in (mm/dd/yy hh:mm) : ")
		
			if re.search(r'\d\d\/\d\d\/\d\d\s\d\d:\d\d',startTime) and re.search(r'\d\d\/\d\d\/\d\d\s\d\d:\d\d',endTime):
				break
			else:
				print ("Wrong Format Entered. \n Please Enter Again !!")
		timeBasedLog(startTime,endTime)
	
	showOutput()
				
userInput()

