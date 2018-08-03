#!/bin/python 
# A helper file to subnetScan.py for Class B IP addresses

import socket


# Description: Determine if subnet mask is correct for class B address
# Input: string array of each subnet byte
# Return: false if incorrect subnet mask for Class B address, otherwise true
def validBSub(subnetArr):
     
    if (subnetArr[0] != '255' ) | (subnetArr[1] != '255'):
        return False
    
    #Default B mask
    if(subnetArr[2] == '0') & (subnetArr[3] == '0'):
        return True

    currPos = 128
    currHalf = 64
    currBool = False
    lastNum = 0
    currByte = int(subnetArr[2])
    
    # Go through 3rd byte and check if correct
    for i in range(1,7):
        if (currByte == currPos):
            currBool = True
            lastNum = currPos
        currPos = currPos + currHalf
        currHalf = currHalf/2
    
    # Check last byte
    if ((lastNum == 255) & (int(subnetArr[3]) > 0) )| (currBool == False):
        return False
    
    currPos = 128
    currHalf = 64
    currBool = False
    currByte = int(subnetArr[3])

    # Go through 4th byte and check if correct
    for i in range(1,7):
        if (currByte == currPos):
            currBool = True
        currPos = currPos + currHalf
        currHalf = currHalf/2

    return currBool


# Description: Go through B subnet and make connection with all IPs 
# and print active addresses with host names
# Input: String arrays for trgtIP and subnetMask
# Output: void
def subnetBScan(trgtIP, subnetMask):
    
    #Get the blockSize of subnet and correct starting IP of subnet
    thirdByte = int(subnetMask[2])
    blockSize = 256 - thirdByte
    subStart = int(trgtIP[2]) % blockSize
    correctSubnet = int(trgtIP[2]) - subStart
    
    lastByte = int(subnetMask[3])
    lastBlkSize = 256 - lastByte
    lastStart = int(trgtIP[3]) % lastBlkSize
    correctSubnet2 = int(trgtIP[3]) - lastStart
    
    # If fourth octet is zero 
    if( lastByte == 0):
        start = correctSubnet
        end = correctSubnet + blockSize 

        for thirdOct in range(start,end):
            for fourthOct in range(1,255): 
                currIP = str(trgtIP[0]+"."+trgtIP[1]+"."+ \
                str(thirdOct)+"."+str(fourthOct))
            
                try:
                    currSock = socket.gethostbyaddr(currIP)
                    line = currIP + " " + currSock[0]
                    print line
                except:
                    pass
    else:

        start = correctSubnet2 + 1
        end = correctSubnet2 + lastBlkSize -1
        
        for i in range(start,end):
            currIP = str(trgtIP[0]+"."+trgtIP[1]+"."+trgtIP[2]+"."+str(i))
            print currIP
            try:
                currSock = socket.gethostbyaddr(currIP)
                line = currIP + " " + currSock[0]
                print line
            except:
                pass

