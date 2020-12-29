import json
import os
from LRUCache import LRUCache

filename = 'filename.txt'
fileHandler = open(filename, 'ab+')


def writeFile(data):
    global fileHandler

    try:
        delLast()
        fileHandler.seek(0, os.SEEK_END)
        res = (', '+json.dumps(data)[1:]).encode()
        fileHandler.write(res)
    except:
        fileHandler.write(json.dumps(data).encode())
    fileHandler.flush()


def readFile():
    global fileHandler
    fileHandler.seek(0, 0)
    read_data = fileHandler.readline()
    return json.loads(read_data)


def delLast():
    with open(filename, 'rb+') as tempFileHandle:
        tempFileHandle.seek(-1, os.SEEK_END)
        tempFileHandle.truncate()
        tempFileHandle.flush()
        tempFileHandle.close()


def get(key):
    #if existis in lru return else read and (return / error)
    print("")

def add(key,value):
    #key exists in lru/file if yes throw error else add it    
    print("")

def delete(key):
    #delete from file, lru
    #rewrite fully
    print("")

writeFile({'Starspy': 1, 'bfvjbvf': 'Test1', 'sia': 'jkfvb'})
print(readFile())
data = {'mani': 1, 'fhb': 'Test1'}
writeFile(data)
print(readFile())
data = {'asd': 1, 'jfjf': 'Test1', 'jkhfbkfbfjf': 'Test1'}
writeFile(data)
print(readFile())
