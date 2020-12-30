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
            self.fileHandler.seek(0, 0)
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
            open(self.filename, "w").close()
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

    def getValueFromFile(self, key):
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
        if(value is not False):
            return value
        value = self.getValueFromFile(key)
        if(value is not False):
            return value
        raise Exception("Error: Key not found")

    def add(self, key, value):
        value['inserted_at'] = int(time.time())
        data = {key: value}
        if not isinstance(key, str):
            raise Exception("Error: Key must be string")
        if len(key) > 32:
            raise Exception("Error: Length of key should be less 32 chars")
        if(self.cache.get(key) != False or self.getValueFromFile(key) != False):
            raise Exception("Error: Key alerady exists")
        self.writeFile(data)
        self.cache.put(key, value)

    def delete(self, key):
        if not self.deleteFile(key):
            raise Exception("Error: Key not found")
        self.cache.delete(key)


s = SelvaDB("selva.txt")
# s.writeFile({'Starspy': {"data":"1","ttl":10}, 'bfvjbvf': {"data":"vana","ttl":100}, 'sia': {"data":"mmnyf","ttl":100}})
# print(s.readFile())
s.add("amas", {"data": "amssss", "ttl": 100})
s.add("masssni", {"data": "nandri", "ttl": 100})
print(s.readFile())

s.add("ama", {"jh": "jhg","ttl":2})
print(s.get("amas"))
print(s.get("masssni"))
print(s.readFile())
print(s.delete("masssni"))
print(s.readFile())
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
