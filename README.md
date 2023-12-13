M1 Team:

Edward Xie - xieey - 16356593

Jason Lee - jasonel2 - 26256544

Jooyoung Kim - jooyok3 - 92727848 

Building the Index:
    Uncomment everything under main in main.py before you run it.
    Make sure rename the corpus folder as "DEV" and put them in the same directory as main.py.
    There should be "totalIndex.txt" which is the merged inverted index in disk.
    This process should take a while dpending on how many documents are in the "DEV" folder.

Running the application:
    The application should pop up right after you built the index.
    If not/you have the index file, but you want rerun the application, simply 
    Comment out the following functions:
        #fileDirectory()
        #tfidf()
        #mergeIndex()
        #makeDocFile()
    Make sure to not comment out functions below:
        buildIndexOfIndex()
        retrieveDocId() 
        openCache()

Starting the search engine and how to search:
    Type a query (words or keywords) that you want to search for and type enter.
    The first 10 are the most relevant results for the query the user has typed.
    If no query shows up, that means no documents were related to that query.
    The user can click the top right CS 121 to go back to homepage.