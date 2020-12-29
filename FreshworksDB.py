import json
import os
from LRUCache import LRUCache
import time


class SelvaDB(object):
    def __init__(self, fileName=None):
        if fileName is None:
            self.filename = "filename.txt"
        else:
            self.filename = fileName
        self.cache = LRUCache(10)
        self.fileHandler = open(self.filename, 'wb+')

    def writeFile(self, data):
        try:
            self.delLastFile()
            self.fileHandler.seek(0, os.SEEK_END)
            res = (', '+json.dumps(data)[1:]).encode()
            self.fileHandler.write(res)
        except:
            self.fileHandler.write(json.dumps(data).encode())
        self.fileHandler.flush()

    def readFile(self):
        self.fileHandler.seek(0, 0)
        read_data = self.fileHandler.readline()
        return json.loads(read_data)

    def deleteFile(self, key):
        data = self.readFile()
        if key in data.keys():
            del data[key]
            open('file.txt', 'w').close()
            self.writeFile(data)
            # instead of using two different file handler for truncate file and writing updated value
            # we can use single file handler, where both truncate and write can be done
            # like, one join query is better than two diff select query to query engine
            # considering code resubality, here i simply invoked writeFile function
            return True
        else:
            return False

    def delLastFile(self,):
        with open(self.filename, 'rb+') as tempFileHandle:
            tempFileHandle.seek(-1, os.SEEK_END)
            tempFileHandle.truncate()
            tempFileHandle.close()

    def getValueFromDB(self, key):
        self.fileHandler.seek(0, 0)
        fileData = self.fileHandler.readline()
        if(fileData == b''):
            return False
        read_data = json.loads(fileData)
        if key in read_data.keys():
            return read_data[key]
        else:
            return False

    def get(self, key):
        value = self.cache.get(key)
        if(value == False):
            value = self.getValueFromDB(key)
            if(value == False):
                raise Exception("Error: Key not found")
        return value

    def add(self, key, value):
        value['inserted_at'] = int(time.time())
        data = {key: value}
        if isinstance(key, str):
            if len(key) <= 32:
                if(self.cache.get(key) != False or self.getValueFromDB(key) != False):
                    raise Exception("Error: Key alerady exists")
                else:
                    self.writeFile(data)
                    self.cache.put(key, value)
            else:
                raise Exception("Error: Length of key should be less 32 chars")
        else:
            raise Exception("Error: Key must be string")

    def delete(self, key):
        if self.deleteFile(key):
            self.cache.delete(key)
        else:
            raise Exception("Error: Key not found")


# filename = 'filename.txt'
# fileHandler = open(filename, 'wb+')
# cache = LRUCache(10)
# def writeFile(data):
#     global fileHandler
#     try:
#         delLastFile()
#         fileHandler.seek(0, os.SEEK_END)
#         res = (', '+json.dumps(data)[1:]).encode()
#         fileHandler.write(res)
#     except:
#         fileHandler.write(json.dumps(data).encode())
#     fileHandler.flush()
# def readFile():
#     global fileHandler
#     fileHandler.seek(0, 0)
#     read_data = fileHandler.readline()
#     return json.loads(read_data)
# def deleteFile(key):
#     data = readFile()
#     if key in data.keys():
#         del data[key]
#         open('file.txt', 'w').close()
#         writeFile(data)
#         # instead of using two different file handler for truncate file and writing updated value
#         # we can use single file handler, where both truncate and write can be done
#         # like, one join query is better than two diff select query to query engine
#         # considering code resubality, here i simply invoked writeFile function
#         return True
#     else:
#         return False
# def delLastFile():
#     with open(filename, 'rb+') as tempFileHandle:
#         tempFileHandle.seek(-1, os.SEEK_END)
#         tempFileHandle.truncate()
#         tempFileHandle.close()
# def getValueFromDB(key):
#     fileHandler.seek(0, 0)
#     read_data = json.loads(fileHandler.readline())
#     if key in read_data.keys():
#         return read_data[key]
#     else:
#         return False
# def get(key):
#     value = cache.get(key)
#     if(value == False):
#         value = getValueFromDB(key)
#         if(value == False):
#             raise Exception("Error: Key not found")
#     return value
# def add(key, value):
#     data = {key: value}
#     if isinstance(key, str):
#         if len(key) <= 32:
#             if(cache.get(key) != False or getValueFromDB(key) != False):
#                 raise Exception("Error: Key alerady exists")
#             else:
#                 writeFile(data)
#                 cache.put(key, value)
#         else:
#             raise Exception("Error: Length of key should be less 32 chars")
#     else:
#         raise Exception("Error: Key must be string")
# def delete(key):
#     if deleteFile(key):
#         cache.delete(key)
#     else:
#         raise Exception("Error: Key not found")
s = SelvaDB()
# s.writeFile({'Starspy': {"data":"1","ttl":10}, 'bfvjbvf': {"data":"vana","ttl":100}, 'sia': {"data":"mmnyf","ttl":100}})
# print(s.readFile())
s.add("amas", {"data": "amssss", "ttl": 100})
s.add("masssni", {"data": "nandri", "ttl": 100})
print(s.readFile())

# s.add("ama", "aty")
# print(s.get("amas"))
# print(s.get("mani"))
# print(readFile())
# delete('ama')
# print(readFile())
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
