#!/bin/python 
# A helper file to subnetScan.py for Class B IP addresses

import socket


# Description: Determine if subnet mask is correct for class B address
# Input: string array of each subnet byte
# Return: false if incorrect subnet mask for Class B address, otherwise true
def validCSub(subnetArr):
     
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
