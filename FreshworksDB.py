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
        self.deleteList = []
        self.cache = LRUCache(10)
        self.fileHandler = open(self.filename, 'wb+')

    def throwException(self, data):
        self.commit()
        raise Exception(data)

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
            self.deleteList.append(key)
            return True
            # del data[key]
            # open(self.filename, "w").close()
            # self.writeFile(data)
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
        if key in self.deleteList:
            self.throwException("Error: Key not found")
        print("hjg")
        value = self.cache.get(key)
        if(value is not False and ('ttl' not in value.keys() or ('ttl' in value.keys() and (int(time.time()) - value['inserted_at'] <= value['ttl'])))):
            return value
        value = self.getValueFromFile(key)
        if(value is not False and ('ttl' not in value.keys() or ('ttl' in value.keys() and (int(time.time()) - value['inserted_at'] <= value['ttl'])))):
            return value
        if(value is not False):
            self.deleteList.append(key)
        self.throwException("Error: Key not found")

    def add(self, key, value):
        data = {key: value}
        if not isinstance(key, str):
            self.throwException("Error: Key must be string")
        if len(key) > 32:
            self.throwException("Error: Length of key should be less than or equal to 32 chars")
        if(self.cache.get(key) != False or self.getValueFromFile(key) != False):
            self.throwException("Error: Key alerady exists")
        if not isinstance(value, dict):
            self.throwException("Error: Value must be json")
        if (len(str(value))/1024) > 16:
            self.throwException("Error: Size of value should be less than or equal to 16KB")
        if key in self.deleteList:
            self.deleteList.remove(key)

        value['inserted_at'] = int(time.time())
        self.writeFile(data)
        self.cache.put(key, value)

    def delete(self, key):
        if not self.deleteFile(key):
            self.throwException("Error: Key not found")
        self.cache.delete(key)

    def commit(self):
        if len(self.deleteList) > 0:
            data = self.readFile()
            for key in self.deleteList:
                if key in data.keys():
                    del data[key]
            print(data)
            with open(self.filename, "w") as f:
                f.close()
            self.writeFile(data)


s = SelvaDB("selva.txt")
# s.writeFile({'Starspy': {"data":"1","ttl":10}, 'bfvjbvf': {"data":"vana","ttl":100}, 'sia': {"data":"mmnyf","ttl":100}})
# print(s.readFile())
s.add("amas", {"data": "amssss", })
s.add("masssni", {"mani": "amssss",} )
# s.add("masssni", {"data": "nandri", "ttl": 100})
s.add("kjhg", {"jh": "jhg", "ttl": 2})
print(s.readFile())
print(s.get("amas"))
# print(s.get("masssni"))
a = input()
print(s.get("kjhg"))
# print(s.get("masssni"))
# print(s.readFile())
# print(s.delete("masssni"))
s.commit()
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
