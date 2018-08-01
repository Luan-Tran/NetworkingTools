#!/bin/python 

'''
Author: Luan Tran
Date: 7/22/18
Description: A simple script that pings all the local hosts on a subnet.
    Main function prints the active IPs and hostsnames into a file terminal. 
    User must provide the IP address in the subnet and the subnet 
    mask. Works for Class B and C IP networks.
'''

import optparse
import errno
import cScan
import bScan

# Description: Check for length and numeric characters
# Input: IP and subnet string arrays
# Output: True if IP and subnet are 4 bytes and numeric, false otherwise
def validIpAndSubStruct(ipCheckStrings, subnetCheckStrings):
    
    error = "Incorrect IP address or subnet mask"

    #Check for correct length
    if (len(ipCheckStrings) != 4) | (len(subnetCheckStrings) != 4):
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
    
    bScan.subnetBScan(ipCheckStrings, subnetCheckStrings)
    if (validIpAndSubStruct(ipCheckStrings,subnetCheckStrings) == False):
        print parser.usage
        exit(0)
    
    # Scan subnet
    ipClass = int(ipCheckStrings[0])
    if ipClass >= 128 & ipClass <= 191:
        if cScan.validCSub(subnetCheckStrings) == False:
            print parser.usage
            exit(0)
        else:
            cScan.subnetCScan(ipCheckStrings, subnetCheckStrings)
    elif ipClass >= 192 & ipClass <= 223:
        if bScan.validBSub(subnetCheckStrings) == False:
            print parser.usage
            exit(0)
        else:
            bScan.subnetBScan(ipCheckStrings, subnetCheckStrings)
    else:
        print parser.usage
        exit(0)
    
if __name__ == "__main__":
    main()

    
