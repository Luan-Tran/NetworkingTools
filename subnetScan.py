#!/bin/python 

'''
Author: Luan Tran
Date: 7/22/18
Description: A simple script that pings all the local hosts on a subnet.
    Main function prints the active IPs and hostsnames into a file or to 
    terminal. User must provide the IP address in the subnet and the subnet 
    mask. Currently only works for Class C IP addresses
'''

import optparse
import os
import errno
import socket

#Go through subnet and make connection with all IPs and print active addresses
def subnetScan(trgtIP, subnetMask):
    
    #Get the blockSize of subnet and correct starting IP of subnet
    blockSize = 256- int(subnetMask[3])
    subStart = int(trgtIP[3]) % blockSize
    correctSubnet = int(trgtIP[3]) - subStart

    
    # Go through subnet and make a connection with each host, 
    # print active IPs to file or terminal
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

# Returns false if incorrect subnet mask, otherwise true
def validSub(lastByte):

    if(lastByte == 0):
        return True
    
    currPos = 128
    currHalf = 64
    currBool = False

    for i in range(1,7):
        currBool = (currBool) | (lastByte == currPos)
        currPos = currPos + currHalf
        currHalf = currHalf/2
    
    return currBool

def validIpAndSub(ipCheckStrings, subnetCheckStrings):
    
    error = "Incorrect IP address or subnet mask"

    #Check for correct length
    if (len(ipCheckStrings) != 4) | (len(subnetCheckStrings) != 4):
        print 'here'
        print error
        return False

    for i in range(4):
        ipByte = ipCheckStrings[i]
        subnetByte = subnetCheckStrings[i]
        
        #Check for digits only
        if (ipByte.isdigit() == False) | (subnetByte.isdigit() == False):
            print error
            return False

        #Check if range is correct
        ipNum = int(ipByte)
        subnetNum = int(subnetByte)
        if (ipNum > 255) | (subnetNum > 255):
            print error
            return False
        
        #Check for valid C subnet mask
        if( i == 3) & (validSub(subnetNum) == False):
            print error 
            return False

    return True


def main():
    #Argument options
    parser = optparse.OptionParser("usage %prog -H <IP address> -S <subnet" + \
    "mask> ")
    parser.add_option("-H", dest = "trgtIP", type = "string", help = \
    "specify target IP address")
    parser.add_option("-S", dest = "trgtSubnet", type = "string", help = \
    "specify subnet mask")
    
    #Assign arugments
    (options,args) = parser.parse_args()
    trgtIP = options.trgtIP
    subnetMask = options.trgtSubnet
    
    #Check if arugments were passed in
    if (trgtIP == None) | (subnetMask == None):
        print parser.usage
        exit(0)

    #Check if IP and subnet are valid
    ipCheckStrings = trgtIP.split('.')
    subnetCheckStrings = subnetMask.split('.')
    if (validIpAndSub(ipCheckStrings,subnetCheckStrings) == False):
        print parser.usage
        exit(0)

    
    #Scan subnet
    subnetScan(ipCheckStrings,subnetCheckStrings)


if __name__ == "__main__":
    main()

    
