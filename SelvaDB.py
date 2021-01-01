import json
import os
from LRUCache import LRUCache
import time
from random import randint
from threading import Lock
from FileHandler import FileHandler


class SelvaDB(object):
    '''
    This is the main class for the Key-Value store database.
    to store recent data, LRU cache is used
       -> size of this cache has to determined
           1. It shouldn't be minimum, because page replacements will be frequent
           2. It can't be huge too. because this itself may occupy more space
    '''

    def __init__(self,fileName = None):
        '''
            create new file object -> to handle read and write operation in file
        '''
        self.fh = FileHandler(fileName)
        self.deleteList = []
        self.cache = LRUCache(20)
        self.lock = Lock()

    def throwException(self, data):
        '''
           This is helper method for throw exception
           -> commit all changes before throwing exception
           -> go to commit method, for more info
        '''
        self.fh.commit(self.deleteList)
        self.deleteList.clear()
        raise Exception(data)

    def getValueFromFile(self, key):
        '''
            If key is not available in LRU, then read from file
            if key is not there then return false
        '''
        try:
            data = self.fh.readFile()
            if key in data.keys():
                return data[key]
        except:
            pass
        return False


    def get(self, key):
        '''
            To get the value from db
            check data exist in LRU or File
            incase of key is there, check data is alive by checking (current epoch - inserted_at of data > time to live), then return value
            otherwise key not found
       '''
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
        '''
        To insert new key value in db
        while inserting we are adding inserted_at property
           This is similar to adding inserted_at columns in sql databases. default value - current timestamp - here we used epoch
           sql query  - col2 datetime not null default(current_timestamp)
           In this it throws an error - with respect to functional requirements
       '''
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
        '''
        Delete data from file
        key in deletelist -> already delete call was invoked for this particular key, so throw exception
        key not in file -> this particular key is never added. so throw exception
        otherwise add this key in deleteList - this has to be deleted
        later this can be deleted by calling commit method

        Thread Safe
        when many threads are calling, data consistency may not be there
        ideally, when a read operation made by thread - always it should get the last updated value 
        in our case, it should get data or not depends on delete operation
        
        by using lock(a concept from operating systems) this delete operation can be called by only one thread at a time
        '''
        self.lock.acquire()
        data = self.fh.readFile()
        if key in self.deleteList or key not in data.keys():
            self.throwException("Error: Key not found")
        self.deleteList.append(key)
        self.lock.release()
