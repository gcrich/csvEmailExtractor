#!/usr/bin/python
#
# csvEmailExtractor.py
#
# reads from a CSV file with a rather strict / narrow schema
# from this CSV file (specified at runtime on command line), this script
# produces terminal output that can be copy/pasted into address line
# of email clients for nicely formatted email lists
#
# usage example:
#   python csvEmailExtractor.py m7s.csv
#       this will parse the file named m7s.csv
#       if no filename argument is supplied, the default value is
#       \'cevnsCommunity.csv'
#
# created ... sometime in the past by GCRich
#
#

from __future__ import print_function

import csv
import argparse


argParser = argparse.ArgumentParser()
argParser.add_argument('csvFilename', type=str, default='cevnsCommunity.csv',
                        nargs='?',
                        help='Filename of the CSV file to parse')

parsedArgs = argParser.parse_args()
inputFilename = parsedArgs.csvFilename
    

        
        
# keep track of any entries in CSV file that seem problematic
entriesWithIssues = []

#
# keep track of whether or not we have the skip email column in this list
# skip email column is defined as a column with header 'Receive all emails?'
# if there is a value of 'n' in this for a given address, do not include
# this person in every mailing
#
# the list of people with this flag will be printed out separately from
# main list
skipEmailFlagColumnHeader = 'Receive all emails?'
hasSkipEmailFlag = False

# keep track of any entries that are flagged as not receiving all emails
skippedAddresses = []

with open(inputFilename, 'r') as rawInputFile:
    dictreader = csv.DictReader(rawInputFile)
    
    print('CSV file appears to have the following fields...')
    for field in dictreader.fieldnames:
        print(field)
        if field == skipEmailFlagColumnHeader:
            hasSkipEmailFlag = True
    
    print('\n\n')
    if hasSkipEmailFlag == True:
        print('Found skip-email column\n')
    else:
        print('Did not find column designating addresses for skipping in some mailings\n')
        
    print('\n\nADDRESS LIST BELOW.. COPY/PASTE INTO BCC LINE OF EMAIL\n\n')
    
    # sloppy error checking but i'm feeling lazy
    if 'Surname' in dictreader.fieldnames and 'Given name' in dictreader.fieldnames and 'email' in dictreader.fieldnames:
        for row in dictreader:
            if row['Surname'] == '' or row['Given name'] == '' or row['email'] == '':
                entriesWithIssues.append(row)
                continue
            if hasSkipEmailFlag:
                if row[skipEmailFlagColumnHeader] == 'n':
                    skippedAddresses.append('\"{}, {}\" <{}>,'.format(row['Surname'], row['Given name'], row['email']))
                    continue
            print('\"{}, {}\" <{}>,'.format(row['Surname'], row['Given name'], row['email']))
            
    elif 'Name' in dictreader.fieldnames and 'email' in dictreader.fieldnames:
        for row in dictreader:
            if row['Name'] == '' or row['email'] == '':
                entriesWithIssues.append(row)
            print('\"{}\" <{}>,'.format(row['Name'], row['email']))
        
    else: # if you get here, some combination of recognizable fields isn't present
        print('\n\nERROR\n\nCSV file seems badly formed for this fragile parser\n\n')
        

print('\n\n------------ END OF MAIN LIST OF ADDRESSEES ------------\n\n')

if len(skippedAddresses) != 0:
    print('\n\nPRINTING ADDRESSEES **NOT** INTENDED TO RECIEVE ALL MAILINGS -- INCLUDE WITH CARE\n\n')
    for skipped in skippedAddresses:
        print(skipped)
    print('\n')
    
if len(entriesWithIssues) != 0:
    print('\n\n\nPROBLEMATIC ENTRIES\n')
    for problematicEntry in entriesWithIssues:
        print('Problem with entry: {}, {}, {}'.format(problematicEntry['Surname'], 
              problematicEntry['Given name'], problematicEntry['email']))
else:
    print('\n\n\n')
    print('No problems with entries!')
