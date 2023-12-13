import json
from pathlib import Path
from bs4 import BeautifulSoup
import math
from sys import getsizeof
import pickle
import pprint
import collections 
import os
import time
import linecache
# object called posting that contains docid, tfidf score, and if this posting contains an important word (boolean value)


class Posting:
    def __init__(self, docid, tfidf, importantWord): 
        self.docid = docid
        self.tfidf = tfidf
        self.importantWord = importantWord

# no longer needed. We have web interface.
"""def queryFromCmdLine():
    #print("This is the name of the program:", sys.argv[0])
    #print("Number of elements including the name of the program:", len(sys.argv)) 
    #print("Argument list: ", str(sys.argv))
    for i in range(1, len(sys.argv)):
        query.append(sys.argv[i])"""

inverted_index = {}
doc_id = {}
numOfDocs = 0
queueIndex = collections.deque([])
indexOfIndex = {}
doc_ids = {}

# reads all the files from folder_name DEV and returns a list of all of their json data
def fileDirectory(folder_name ='DEV'):  
    indexNum = 1
    docCount = 0
    p = Path(folder_name)
    for posixPath in list(p.glob('**/*.json')):
        if docCount > 10000:
            # create partial index
            writePartialIndex(indexNum)
            indexNum += 1
            docCount = 0
        else:
            # add to index
            print(docCount)
            f = open(posixPath)
            data = json.load(f)
            buildIndex(data)
            docCount += 1
    if docCount > 0:
        writePartialIndex(indexNum)

def writePartialIndex(indexCount):
    filename = "index" + str(indexCount) + ".txt"
    fileobj = open(filename, 'wb')
    sortDict()
    pickle.dump(inverted_index, fileobj)
    fileobj.close()
    inverted_index.clear()
    queueIndex.append(filename)

def sortDict():
    global inverted_index
    myKeys = list(inverted_index.keys())
    myKeys.sort()
    inverted_index = {i: inverted_index[i] for i in myKeys}

def buildIndex(doc):
    global numOfDocs
    doc_id[numOfDocs] = doc['url']
    token_count = {}
    tokens, importantTokens = scrapeText(doc)
    uniqueImportantTokens = set(importantTokens)
    uniquetokens = set(tokens)
    numOfWords = len(tokens)
    for token in tokens:
        if token not in token_count:
            token_count[token] = 1
        else:
            token_count[token] += 1
        if token not in inverted_index:
            inverted_index[token] = []
    for token in uniquetokens:
        if token in uniqueImportantTokens:
            #index[token].append(Posting(n, 1 + math.log(token_count[token]/numOfWords, 10), True))
            inverted_index[token].append(Posting(numOfDocs, token_count[token]/numOfWords, True))
        else:
            inverted_index[token].append(Posting(numOfDocs, token_count[token]/numOfWords, False))
    numOfDocs += 1

def makeDocFile():
    with open("doc_id.txt", "w") as file:
        file.write(str(doc_id))

def tfidf():
    global numOfDocs
    for key in inverted_index:
        idf = math.log(numOfDocs/len(inverted_index[key]), 10)
        for i in range(len(inverted_index[key])):
            #print("previous", index[key][i].docid, index[key][i].tfidf)
            inverted_index[key][i] = Posting(inverted_index[key][i].docid, inverted_index[key][i].tfidf * idf, inverted_index[key][i].importantWord)
            #print("After", index[key][i].docid, index[key][i].tfidf)

def mergeIndex():
    existing_tokens = set()
    while len(queueIndex) != 0:
        filename = queueIndex.popleft()
        fileobj = open(filename, 'rb')
        dictLoad = pickle.load(fileobj)
        with open("totalIndex.txt", "a+") as file:
            file.seek(0)
            lines = file.readlines()
            file.seek(0)
            for token in dictLoad:
                # if word already exists, then rewrite that line
                if token in existing_tokens:
                    word = []
                    for i, line in enumerate(lines):
                        if token == line.strip().split()[0]:
                            word.append(lines.pop(i))
                            break
                    lines.append(word[0].strip("\n") + " " + f"{' '.join([f'{posting.docid}/{posting.tfidf}/{posting.importantWord}' for posting in dictLoad[token]])}\n")
                    #lines.append(f"{token} {' '.join([f'{posting.docid}/{posting.tfidf}/{posting.importantWord}' for posting in dictLoad[token]])}\n")
                else:
                    lines.append(f"{token} {' '.join([f'{posting.docid}/{posting.tfidf}/{posting.importantWord}' for posting in dictLoad[token]])}\n")
                    existing_tokens.add(token)
            file.truncate()
            file.writelines(lines)
        file.close()
    print(len(existing_tokens))

def buildIndexOfIndex():
    with open('totalIndex.txt', 'r') as file:
        lineNumber = 1
        for line in file:
            token = line.strip().split()[0]
            indexOfIndex[token] = lineNumber
            lineNumber += 1
    file.close()

# given a json, if their text length is less than 300 (we know it will be useless information), so we skip that doc
# else, tokenize the parsed text and find their important words (html title tag, headings tag, bolded tag, strong tag, etc...)
# returns a list of tokenized words and a list of important words
def scrapeText(json_data):
    soup = BeautifulSoup(json_data["content"], features="html.parser")
    text = soup.get_text(strip=True, separator=' ')
    store_words = parseGivenText(text)

    title = soup.find('title')
    h1 = soup.find('h1')
    h2 = soup.find('h2')
    h3 = soup.find('h3')
    bold = soup.find('b')
    strong = soup.find('strong')
  
    listOfTitleText = checkTag(title)
    listOfh1Text = checkTag(h1)
    listOfh2Text = checkTag(h2)
    listOfh3Text = checkTag(h3)
    listOfBoldText = checkTag(bold)
    listOfStrongText = checkTag(strong)
    important_words = listOfTitleText + listOfh1Text + listOfh2Text + listOfh3Text + listOfBoldText + listOfStrongText
    
    return store_words, important_words

# ------------ begin helper function ------------

# intersect 2 postings into a list
def intersect(p1, p2): 
    answer = []
    ptr1 = 0
    ptr2 = 0
    while ptr1 < len(p1) and ptr2 < len(p2):
        if p1[ptr1].docid == p2[ptr2].docid:
            answer.append(p1[ptr1])
            ptr1 += 1
            ptr2 += 1
        elif p1[ptr1].docid < p2[ptr2].docid:
            ptr1 += 1
        else:
            ptr2 += 1   
    return answer

# tokenize given text
def parseGivenText(text):
    store_words = []
    while True:
        list_of_chars = []
        for c in text:
            if c.isalpha() and c.isascii():
                list_of_chars.append(c.lower())
            else:
                if list_of_chars:
                    text_word = ''.join(list_of_chars)
                    #if text_word not in stop_words:
                    #        store_words.append(text_word)
                    store_words.append(text_word)
                    list_of_chars = []
        if list_of_chars:
                store_words.append(''.join(list_of_chars))
                list_of_chars = []
                #if text_word not in stop_words:
                #    store_words.append(text_word)
        break
    return store_words

# checks if tag is a null value
def checkTag(tag):
    if tag != None:
        res = parseGivenText(tag.get_text(strip=True, separator=' '))
    else:
        res = []
    return res
# ------------ end helper function ------------

# merge all the list of postings in the listofPostings into a list
def intersectAllPostings(listOfPostings):    # [[], []]
    # print(listOfPostings)
    
    if len(listOfPostings) == 0:
        return []
    if len(listOfPostings) == 1:
        return listOfPostings[0]
    if len(listOfPostings) > 1:
        # listOfPostings.sort(key = len)
        initial = intersect(listOfPostings[0], listOfPostings[1])
        for i in range(2, len(listOfPostings)):
            initial = intersect(initial,  listOfPostings[i])
        return initial

# given our index and a query, go through each query term and add it to a list that contains a list of postings.
# ['cristina', 'lopes']

def openCache():
    #st = time.time()
    # ???
    linecache.getline('totalIndex.txt', 10000)
    #et = time.time()
    #exe_time = (et-st)*1000
    #print(exe_time)

def booleanSearch(query):
    listOflineNumbers = []
    for i in range(len(query)):
        if query[i] in indexOfIndex:
            listOflineNumbers.append(indexOfIndex[query[i]])
    with open('totalIndex.txt', 'r') as file:
        listOfPostings = []
        for lineNumber in listOflineNumbers:
            temp =  []
            st = time.time()
            line = linecache.getline('totalIndex.txt', lineNumber) 
            et = time.time()
            exe_time = (et-st)*1000
            print(exe_time)
            postings = line.strip().split()[1:] # postings = ['0/0.82377/false', '0/0.82377/true']
            for posting in postings:
                post = posting.split("/")
                temp.append(Posting(post[0], post[1], post[2]))
            listOfPostings.append(temp)
    file.close()
    return intersectAllPostings(listOfPostings)

"""def booleanSearch(index, query):
    listOfPostings = []
    for i in range(len(query)):
        if query[i] in index:
            listOfPostings.append(index[query[i]])
    return intersectAllPostings(listOfPostings)"""

# displays top 10 urls
def displayTop10Postings(postings, doc_id):
    # postings.sort(key=lambda x : (x.importantWord, x.tfidf), reverse = True)
    if len(postings) < 10:
        for i in range(len(postings)):
            print(doc_id[postings[i].docid])
    else:
        for i in range(10):
            print(doc_id[postings[i].docid])

# returns a list of top 10 most relevant urls
def returnTop10Postings(postings):
    res = []
    postings.sort(key=lambda x : (x.importantWord, x.tfidf), reverse = True) 
    """for posting in postings:
        print(posting.docid, posting.tfidf, posting.importantWord)"""
    
    if len(postings) < 10:
        for i in range(len(postings)):
            res.append(doc_ids[int(postings[i].docid)])   
    else:
        for i in range(10):
            res.append(doc_ids[int(postings[i].docid)])        
    
    return res

# retrieve doc_id from disk 
def retrieveDocId():
    global doc_ids
    with open("doc_id.txt", "r") as file:
        line = file.readline()
        doc_ids = eval(line)
    
# porter stemming to get even more accurate results. Didn't implement into our search engine. Been getting worse results by stemming.
def porterStemming(string, p):
    output = ''
    word = ''
    if string == '':
        return
    if string[-1] != " ":
        string += " "
    for c in string:
        if c.isalpha():
            word += c.lower()
        else:
            if word:
                output += p.stem(word, 0, len(word) - 1)
                word = ''
            output += c.lower()
    return output

if __name__ == "__main__":
    fileDirectory()
    tfidf()
    mergeIndex()
    buildIndexOfIndex()
    makeDocFile()
    retrieveDocId()