#/usr/bin/env python

import sys
import telnetlib
from time import sleep

HOST = raw_input("Enter your host IP : ")
user = raw_input("Enter your username : ")
password = raw_input("Enter your password : ")

tn = telnetlib.Telnet(HOST)

tn.read_until("Login:")
tn.write(user + "\r\n")

tn.read_until("Password: ")
tn.write(password + "\n")

tn.write("config cli more false\n")
command = raw_input("Enter command separated by '(,)' maximum 10: ")
while(1):
	
	#command = raw_input("Enter command separated by '(,)' maximum 10: ")
	choice=raw_input("Select from below options (1 or 2) \n1.Enter no.of iterations \n2.Enter the Time gap \n")
        if (choice=='1'):
		noOfIteration=raw_input("How many times do you want to run each command?? ")
	        command=command.split(',')
        	for i in range (0,int(noOfIteration)):
                	for item in command:
                                tn.write(item + "\n")
                                while(1):

                                        a= tn.read_until("\r\n",1)
                                        if (a):
                                                print (a)
                                                continue
                                        break
	elif(choice=='2'):
		sleep_time=raw_input("Enter the time gap between two output: ") 
		command=command.split(',')
		while(1):
			for item in command:
				tn.write(item + "\n")
				while(1):
					
					a= tn.read_until("\r\n",1)
					if (a):
						print (a)
						continue
					break
                        sleep(int(sleep_time))
        else:
		print("Invalid choice,please select either 1 or 2 ")
                continue
	break
tn.write("exit\n")
