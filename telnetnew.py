#!/usr/bin/env python

import telnetlib
import threading
import os.path
import subprocess
import time
import sys


#Checking IP address validity
def ip_is_valid():
    check = False
    global ip_list
    global port_list
    global ips
    global ports

    ips = []
    ports = []
    
    
    #Prompting user for input
    ip_file = raw_input("Enter IP file name and extension: ")
                
        
    #Open user selected file for reading (IP addresses file)
    selected_ip_file = open(ip_file, 'r')
            
            #Starting from the beginning of the file
    selected_ip_file.seek(0)
            
            #Reading each line (IP address) in the file
    ip_list = selected_ip_file.readlines()

            #forming IP's list
    for item in ip_list:
        ips.append(item.strip().split(':')[0])
    #forming ports list
    for item in ip_list:
        ports.append(item.strip().split(':')[1])


    print ips
    print ports
            
            #Closing the file
    selected_ip_file.close()
            


#Checking command file validity
def cmd_is_valid():
    global cmd_file

    while True:
        cmd_file = raw_input("Enter command file name and extension: ")

        #Changing exception message
        if os.path.isfile(cmd_file) == True:
            print "\nSending command(s) to device(s)...\n"
            break

        else:
            print "\nFile %s does not exist! Please check and try again!\n" % cmd_file
            continue

#Change exception message
try:
    #Calling IP validity function
    ip_is_valid()

except KeyboardInterrupt:
    print "\n\nProgram aborted by user. Exiting...\n"
    sys.exit()


#Open telnet connection to devices
def open_telnet_conn(ip,port):
    #Change exception message
    try:
        #Define telnet parameters
        username = 'taman'
        password = 'test'
        
        #Specify the Telnet port (default is 23, anyway)
        
        #Specify the connection timeout in seconds for blocking operations, like the connection attempt
        connection_timeout = 5
        
        #Specify a timeout in seconds. Read until the string is found or until the timout has passed
        reading_timeout = 5
        
        #Logging into device
        connection = telnetlib.Telnet(ip, port, connection_timeout)
        
        #Waiting to be asked for an username
        router_output = connection.read_until("Username:", reading_timeout)
        #Enter the username when asked and a "\n" for Enter
        connection.write(username + "\n")
        
        #Waiting to be asked for a password
        router_output = connection.read_until("Password:", reading_timeout)
        #Enter the password when asked and a "\n" for Enter
        connection.write(password + "\n")
        time.sleep(1)	
        
        #Setting terminal length for the entire output - disabling pagination
        connection.write("terminal length 0\n")
        time.sleep(1)
        
        #Entering global config mode
        connection.write("\n")
        connection.write("configure terminal\n")
        time.sleep(1)
        

        #GInvoke cmd file from the user
        cmd_is_valid()
        #Open user selected file for readin

        selected_cmd_file = open(cmd_file, 'r')
            
        #Starting from the beginning of the file
        selected_cmd_file.seek(0)
        
        #Writing each line in the file to the device
        for each_line in selected_cmd_file.readlines():
            connection.write(each_line + '\n')
            time.sleep(2)
    
        #Closing the file
        selected_cmd_file.close()
        
        #Test for reading command output
        #router_output = connection.read_very_eager()
        #print router_output
        
        #Closing the connection
        connection.close()
        
    except IOError:
        print "Input parameter error! Please check username, password and file name."



def create_threads():
    
    for ip,port in zip(ips,ports):
        print("Connecting ip:%s and Port:%s" % (ip,port))
        open_telnet_conn(ip,port)   #args is a tuple with a single element
        #th.start()
        #threads.append(th)
        

#Creating threads
#def create_threads():
#   threads = []
#    for ip,port in zip(ips,ports):
#        print("Connecting ip:%s and Port:%s" % (ip,port))
#        th = threading.Thread(target = open_telnet_conn, args = (ip,port))   #args is a tuple with a single element
#        th.start()
#        threads.append(th)
#        
#   for th in threads:
#        th.join()

#Calling threads creation function
create_threads()

#End of program
