#!/bin/python 
# A helper file to subnetScan.py for Class C IP addresses

import socket


# Description: Determine if subnet mask is correct for class C address
# Input: string array of each subnet byte
# Return: false if incorrect subnet mask for Class C address, otherwise true
def validCSub(subnetArr):
    
    if( subnetArr[0] != '255') | (subnetArr[1] != '255') | (subnetArr[2] != '255'):
        return False
    
    #Default mask
    if(subnetArr[3] == '0'):
        return True
    
    currPos = 128
    currHalf = 64
    currBool = False
    lastByte = int(subnetArr[3])
    
    #Check for valid addresses
    for i in range(1,7):
        if( lastByte == currPos):
            currBool = True
        currPos = currPos + currHalf
        currHalf = currHalf/2
    
    return currBool

# Description: Go through C subnet and make connection with all IPs 
# and print active addresses with host names
# Input: String arrays for trgtIP and subnetMask
# Output: void
def subnetCScan(trgtIP, subnetMask):
    
    #Get the blockSize of subnet and correct starting IP of subnet
    blockSize = 256- int(subnetMask[3])
    subStart = int(trgtIP[3]) % blockSize
    correctSubnet = int(trgtIP[3]) - subStart

    
    # Go through subnet and make a connection with each host, 
    # print active IPs terminal
    start = correctSubnet+1
    end = correctSubnet+blockSize-1
    for i in range(start,end):
        currIP = str(trgtIP[0]+"."+trgtIP[1]+"."+trgtIP[2]+"."+str(i))

        try:
            currSock = socket.gethostbyaddr(currIP)
            line = currIP + " " + currSock[0]
            print line
        except:
            pass
