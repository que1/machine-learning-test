# -*- coding: utf8 -*-

import feedparser
import re

# Takes a filename of URL of a blog feed and classifies the entries
def read(feed, classifier):
    # Get feed entries and loop over them
    f = feedparser.parse(feed)
    for entry in f['entries']:
        print()
        print('-----')
        # Print the contents of the entry
        print('Title:     ' + entry['title'].encode('utf-8'))
        print('Publisher: ' + entry['publisher'].encode('utf-8'))
        print()
        print(entry['summary'].encode('utf-8'))

        # Combine all the text to create one item for the classifier
        fulltext = '%s\n%s\n%s' % (entry['title'], entry['publisher'], entry['summary'])

        # Print the best guess at the current category
        print('Guess: ' + str(classifier.classify(entry)))

        # Ask the user to specify the correct category and train on that
        cl = input('Enter category: ')
        classifier.train(entry, cl)
