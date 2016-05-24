# Walking through http://www.laurentluce.com/posts/twitter-sentiment-analysis-using-python-and-nltk/
# Goal is to make basic sentiment analysis to fully understand concepts

import logging
logging.captureWarnings(True)

# bring in pickle to save trained classifier

import pickle

# Bring in Natural Language Tool Kit library

import nltk

# Library to work with CSV files, what we're storing everything in

import csv

# Define training set(s), the bigger the better

# open csv, put all tweets and sentiments in a dictionary
# iterate through dictionary pulling out all postiive and negative values
# build seperate positive and negative lists

positive_training_tweets = []
negative_training_tweets = []

print "Loading training tweets..."
with open('training_tweets.csv', 'rt') as f:
    theReader = csv.reader(f, delimiter=',')
    for row in theReader:
        if row[1] == '1':
            positive_training_tweets.append((row[3], row[1]))
            #print row[3]
            #print row[1]
        if row[1] == '0':
            negative_training_tweets.append((row[3], row[1]))
            #print row[3]
            #print row[1]

# Define test input to classify

print "Loading test tweets..."
test_tweets = []
with open('test_tweets.csv', 'rt') as f:
    theReader = csv.reader(f, delimiter=',')
    for row in theReader:
        test_tweets.append(row[1])

''' 
FUNCTIONS 
'''

# clean up input, put all in lower case and remove any words less than 3 letters

def tweet_filter(list):
    return_list = []
    for (words, sentiment) in list:
        words_filtered = [letters.lower() for letters in words.split()
        if len(letters) >= 3]
        return_list.append((words_filtered,sentiment))
    return return_list
    
# take out only words from a tweet, sentiment pair and return the words

def get_words_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
        all_words.extend(words)
    return all_words

# create a list of unique features and return just the features, not their distribution

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist) # could just use set() here?
    word_features = wordlist.keys()
    return word_features

# extract features from document

def extract_features(document):
    document_words = set(document) # set creates a list of unique words
    features = {} # empty dict
    for word in word_features: # word_features assigned as get_word_features(get_words_in_tweets(tweets))
        features['contains(%s)' % word] = (word in document_words)
    return features
    
def writeToCSV(string):
    theWriter = csv.writer(open('output.csv', 'ab'))
    theWriter.writerow([string[0],string[1]])

''' 
END FUNCTIONS 
'''

#print "Formatting training tweets..."

tweets = tweet_filter(positive_training_tweets+negative_training_tweets)

word_features = get_word_features(get_words_in_tweets(tweets))

# prepare training set by extracting features

#print "Training classifier...."
#training_set = nltk.classify.apply_features(extract_features,tweets)

# Train Naive Bayes classifier

#classifier = nltk.NaiveBayesClassifier.train(training_set)

#print "Pickling classifier..." 

# save_classifier = open('naivebayes.pickle','wb')
# pickle.dump(classifier, save_classifier)
# # save_classifier.close()

print "Unpickling Classifier..."

pickled_classifier_f = open('naivebayes.pickle', 'rb')
classifier = pickle.load(pickled_classifier_f)
pickled_classifier_f.close()

print "Analyzing test tweets..."

for tweets in test_tweets[(len(test_tweets)-50):(len(test_tweets))]: #just look at sample of test_tweets now
    tweet_to_analyze = str(tweets)
    classifier_guess = (classifier.classify(extract_features(tweet_to_analyze.split())))
    classifier_prob = (classifier.prob_classify(extract_features(tweet_to_analyze.split())))
    print tweets
    print 'Seems like this is ... %s' % str(classifier_guess)
    for classifiers in classifier_prob.samples(): #TO DO wrap in a function to return values to write to csv
        print ('%s: %f' % (classifiers,classifier_prob.prob(classifiers)))
    writeToCSV((tweet_to_analyze,classifier_guess))
    
print classifier.show_most_informative_features(5)

"""
TO DO:
1) add probability, or confidence, to each determined classifier - DONE 5/19/16
2) build additional feature reducers
3) build better trainnig model: movie reviews? larger data set? - Increased training set to 20k tweets 5/20/16
4) determine accuracy by saving 10% of training model to test 
5) save classifier so we don't have to retrain each time https://pythonprogramming.net/pickle-classifier-save-nltk-tutorial/ - DONE 5/20/16
6) add support for emojis
"""
        