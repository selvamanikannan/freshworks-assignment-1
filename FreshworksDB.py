import json
import os
from LRUCache import LRUCache

filename = 'filename.txt'
fileHandler = open(filename, 'rb+')

cache = LRUCache(10)


def writeFile(data):
    global fileHandler
    try:
        delLastFile()
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


def deleteFile(key):
    data = readFile()
    if key in data.keys():
        del data[key]
        open('file.txt', 'w').close()
        writeFile(data)
        # instead of using two different file handler for truncate file and writing updated value
        # we can use single file handler, where both truncate and write can be done
        # like, one join query is better than two diff select query to query engine
        # considering code resubality, here i simply invoked writeFile function
        return True
    else:
        return False


def delLastFile():
    with open(filename, 'rb+') as tempFileHandle:
        tempFileHandle.seek(-1, os.SEEK_END)
        tempFileHandle.truncate()
        tempFileHandle.close()


def getValueFromDB(key):
    fileHandler.seek(0, 0)
    read_data = json.loads(fileHandler.readline())
    if key in read_data.keys():
        return read_data[key]
    else:
        return False


def get(key):
    value = cache.get(key)
    if(value == False):
        value = getValueFromDB(key)
        if(value == False):
            raise Exception("Error: Key not found")
    return value


def add(key, value):
    data = {key: value}
    if isinstance(key, str):
        if len(key) <= 32:
            if(cache.get(key) != False or getValueFromDB(key) != False):
                raise Exception("Error: Key alerady exists")
            else:
                writeFile(data)
                cache.put(key, value)
        else:
            raise Exception("Error: Length of key should be less 32 chars")
    else:
        raise Exception("Error: Key must be string")


def delete(key):
    if deleteFile(key):
        cache.delete(key)
    else:
        raise Exception("Error: Key not found")


writeFile({'Starspy': 1, 'bfvjbvf': 'Test1', 'sia': 'jkfvb'})
print(readFile())
add("amas", "amssss")
add("ama", "aty")
print(readFile())
print(get("amas"))
print(get("ama"))
print(readFile())
delete('ama')
print(readFile())
# delete('amannn')
# add("ama", "aty")
# # add("vnr", "aty")
# # print(readFile())
# # data = {'mani': 1, 'fhb': 'Test1'}
# # writeFile(data)
# # print(readFile())
# # data = {'asd': 1, 'jfjf': 'Test1', 'jkhfbkfbfjf': 'Test1'}
# # writeFile(data)
# # print(readFile())
