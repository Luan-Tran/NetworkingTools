#!/bin/python 
'''
Author: Luan Tran
Date: 8/23/18
Description: A simple script that uses nmap to scan through a list of IP 
    addresses and port numbers to see if the port is open on each IP
    address.
'''
import optparse
import errno
import nmap

def main():
    
    #Argument options
    parser = optparse.OptionParser("usage %prog -F <File> -P <Port " + \
    "numbers> ")
    parser.add_option("-F", dest = "trgtFile", type = "string", help = \
    "specify file with IP addresses")
    parser.add_option("-P", dest = "trgtPortNums", type = "string", help = \
    "specify port numbers, separated by comma")

    #Assign arugments
    (options,args) = parser.parse_args()
    trgtFile = options.trgtFile
    portNums = str(options.trgtPortNums).split(',')

    #Check if arugments were passed in
    if (trgtFile == None) | (portNums == None):
        print parser.usage
        exit(0)
    
    #Read each line into array
    with open(trgtFile) as currLine:
        IPaddresses = currLine.readlines()
    IPaddresses = [x.strip('\n') for x in IPaddresses]


    #Scanner
    scanner = nmap.PortScanner()
    
    #Go through addresses and ports to scan
    for currAdr in IPaddresses:
        for currPort in portNums:
            scanner.scan(currAdr,currPort)
            try:
                state = scanner[currAdr]["tcp"][int(currPort)]["state"]
                print "[*] " + currAdr + " tcp/" + currPort+ " " + state
            except KeyError as exkey:
                print "[-] Cannot scan host: " + currAdr

if __name__ == "__main__":
    main()
