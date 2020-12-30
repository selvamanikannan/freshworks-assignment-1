import json
import os
from LRUCache import LRUCache
import time
from random import randint
from threading import Lock
from FileHandler import FileHandler


class SelvaDB(object):

    def __init__(self,fileName = None):
        self.fh = FileHandler(fileName)
        self.deleteList = []
        self.cache = LRUCache(10)
        self.lock = Lock()

    def throwException(self, data):
        self.fh.commit(self.deleteList)
        self.deleteList.clear()
        raise Exception(data)

    def getValueFromFile(self, key):
        try:
            data = self.fh.readFile()
            if key in data.keys():
                return data[key]
        except:
            pass
        return False


    def get(self, key):
        if key in self.deleteList:
            self.throwException("Error: Key not found")
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
        value['inserted_at'] = int(time.time())

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

        self.fh.writeFile(data)
        self.cache.put(key, value)

    def delete(self, key):
        self.lock.acquire()
        data = self.fh.readFile()
        if key in self.deleteList or key not in data.keys():
            self.throwException("Error: Key not found")
        self.deleteList.append(key)
        self.cache.delete(key)
        self.lock.release()


s = SelvaDB("siva.txt")
# s = SelvaDB("siva")
# s.writeFile({'Starspy': {"data":"1","ttl":10}, 'bfvjbvf': {"data":"vana","ttl":100}, 'sia': {"data":"mmnyf","ttl":100}})
# # print(s.readFile())
s.add("amas", {"data": "amssss", })
s.add("masssni", {"mani": "amssss",} )
# s.add("masssni", {"data": "nandri", "ttl": 100})
s.add("kjhg", {"jh": "jhg", "ttl": 1})
# print(s.readFile())
print(s.get("masssni"))
print(s.delete("masssni"))
print(s.delete("masssni"))
# a = input()
# print(s.get("kjhg"))
# print(s.get("masssni"))
# print(s.readFile())
# print(s.get("masssni"))
# s.commit()
# print(s.readFile())
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
