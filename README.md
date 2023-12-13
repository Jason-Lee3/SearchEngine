# Search Engine Design Document

## Introduction

This document designs a simplified version of a possible Search Engine.

Our document corpus is derived from web pages associated with the Department of Informatics at UCI (ICS). 

The goal of this project is not to build a polished search engine, but rather to introduce the topic of information retrieval in a beginner friendly manner. 

## Background

Information retrieval is _the activity of searching and extracting information from a collection of information resources_. There are different types of Search Engines: Web Search, Vertical Search, Enterprise Search, Desktop Search, and Peer-to-peer Search. This document will only go in-depth about Web Search Engine.

## Requirements
- Query efficiency/speed should be under 300 ms
- Users should get somewhat relevant documents based on their search
- Simple user friendly User Interface
- Utilize some form of ranking formula(s) to rank relevant pages

## High Level Design

<img width="492" alt="Screen Shot 2023-12-12 at 11 19 19 PM" src="https://github.com/Jason-Lee3/SearchEngine/assets/110850240/ff1fdcce-78ed-4de5-bbcd-d668a6d8f018">

### Text Acquisition
Use a web crawler to scrape web pages. This will be our data that users will be able retrieve and search information from.

### Local Document Store
Write those web pages into HTML in the form of JSON files and store them on our disk. 

### Text Transformation/Processing
Tokenize each web page in our local document store. For the search engine we are building, a token will only consist of a sequence of alphanumeric characters, independent of capitalization (so Apple, apple, aPpLe are the same token).

### Index Creation
We will index each term to each document that it pertains to. For instance, a word may map to multiple documents (word1 → doc1 doc2 doc3, word2 → doc1 doc 3, word3 → doc3). 

We will also utilize partial indexing where when we index a or reach certain number of documents, we will write it into a file (into our disk) and clean/clear our in-memory map. This way, we will never run out of memory. Later, we will merge all the partial indexed files into one big index document.

### Index
We will store our index _not_ in memory, but in our disk. This will help us with scalability when we have more documents in the future. 

### Ranking
After building the index, we will use tf-idf, cosine similarity, and important-words to calculate a score for each document, which will help us give more relevant results to the user.

Important-words are words that are in a document/web page's title tag, h1 tag, h2 tag, h3 tag, bolded text, strong words...

### UI
The user interface can be created either through a local GUI or a web GUI.

## Limitations & Future Work
One limitation is that the corpus only contains department of Informatics documents, which means we have less audience for the search engine.

Another limitation is that we are only using three ranking formulas to rank the relevant search, which may give us the precision we want.

In the future, adding more ranking formulas may lead to better user experience and relevant search results. Possibly, utilizing porter stemming to remove commoner morphological and inflexional endings from words may also give us better results. 

# Starting the Search Engine

### Building the Index:
    Uncomment everything under main in main.py before you run it.
    Make sure rename the corpus folder as "DEV" and put them in the same directory as main.py.
    There should be "totalIndex.txt" which is the merged inverted index in disk.
    This process should take a while dpending on how many documents are in the "DEV" folder.

### Running the application:
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

### Starting the search engine and how to search:
    Type a query (words or keywords) that you want to search for and type enter.
    The first 10 are the most relevant results for the query the user has typed.
    If no query shows up, that means no documents were related to that query.
    The user can click the top right CS 121 to go back to homepage.


M1 Team:
Edward Xie - xieey - 16356593
Jason Lee - jasonel2 - 26256544
Jooyoung Kim - jooyok3 - 92727848 
