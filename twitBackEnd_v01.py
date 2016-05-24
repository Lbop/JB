# twitBackEnd calls the Twitter API and retrieves all tweets with "jetblue" keyword
# unique user/tweet/time tweets are stored in JBcsv.csv in the directory
# the api is called every 15 minutes
# Programmed by Derrick Olson 2/19/2016

"""
START FUNCTIONS
"""

# isStringinCSV takes an argument (doesn't need to be a string), and 
# iterates through JBcsv log to see if there is an EXACT match
# returns true if there is a match
# as log file grows, may need to pre-sort log somehow (by user, text first letter, ex.)

def isStringinCSV(stringSample):
    stringInCsvBoolean = False
    with open('JBcsv.csv', 'rt') as f:
        theReader = csv.reader(f, delimiter=",")
        #BUG breaks if CSV is empty
        for row in theReader:
            # print row
            # testvalue = raw_input('Hold after field print in JBcsv.csv')
            if stringSample == row:
                stringInCsvBoolean = True
    return stringInCsvBoolean
    
# writeToCSV takes one argument (doesn't need to be a string), and
# prints the argument, then writes that argument to the log file
# does not return anything, although should return true when 
# successful, or return an error message

def writeToCSV(string):
    print "Writing to CSV:\n%s" % string
    #break writer by using "w" which truncates the file first, a is for appending
    theWriter = csv.writer(open('JBcsv.csv', 'ab'))
    theWriter.writerow([string[0],string[1],string[2]])
    
    #BUG - first line written to a file does not write on a new line
    #BUG? If carriage return in tweet then adds a line to the CSV

"""
END OF FUNCTIONS
"""

"""
TWITTER API SETTINGS
"""

# Keep the "Consumer Secret" a secret. This key should never be human-readable in your application.
# Consumer Key (API Key)
consumerKey = "IMPORT FROM CONFIG"
# Consumer Secret (API Secret)
consumerSecret = "IMPORT FROM CONFIG"
# Access Level	Read and write (modify app permissions)
# Owner	TwainStatistics
# Owner ID	3142527370

# Your Access Token
# This access token can be used to make API requests on your own account's behalf. Do not share your access token secret with anyone.
# Access Token	
accessToken = "IMPORT FROM CONFIG"
# Access Token Secret	
accessSecret = "IMPORT FROM CONFIG"
# Access Level	Read and write
# Owner	TwainStatistics
# Owner ID	3142527370

"""
END OF TWITTER SETTINGS
"""

from TwitterSearch import *
# documentation for library: https://pypi.python.org/pypi/TwitterSearch/

import csv
import time

PreviousTweets = []

keyword1 = 'JetBlue'
keyword2 = 'gate'

def mainLoop():
    try:
        tso = TwitterSearchOrder() # create a TwitterSearchOrder object
        tso.set_keywords([keyword1]) # let's define all words we would like to have a look for
        tso.set_language('en') # we want to see English tweets only
        tso.set_include_entities(False) # and don't give us all the entity information
    
        # create a TwitterSearch object with our secret tokens
        ts = TwitterSearch(
            consumer_key = consumerKey,
            consumer_secret = consumerSecret,
            access_token = accessToken,
            access_token_secret = accessSecret
         )
    # call API
        print "Checking for new tweets that match keywords: %s or %s" % (keyword1,keyword2)
        
        for tweet in ts.search_tweets_iterable(tso):
            
            # bind variables to information from tweets we're interested in
            username = (tweet['user']['screen_name']).encode('ascii', 'replace')
            tweetText = (tweet['text']).encode('ascii', 'replace')
            date = (tweet['created_at']).encode('ascii', 'replace')
            
            if isStringinCSV([username, tweetText, date]) == False: # check to see if individual tweet from TwitterSearch object is in our log
                print "New Tweet!"
                
                writeToCSV([username, tweetText, date]) # if so, write to log
        
        print "Check complete."
        
    except TwitterSearchException as e: # take care of all those ugly errors if there are any
        print(e)
        
while True:
    mainLoop()
    print "Sleeping for 15 minutes..."
    time.sleep(900)