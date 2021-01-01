import json
import os
from LRUCache import LRUCache
import time
from random import randint
from threading import Lock


class FileHandler:
    ''''
       This class handles all read write operations
       DB class will create an object for this
       Only this particular class do read and write operations in file
    '''
    filesUsed = []

    def __init__(self, fileName=None):
        '''
        If filename is provided use the same. otherwise create new file
           constructor overloading
               -> default constructor - create new file
               -> 1 arg constructor - open file with that argument       
        '''
        if fileName is None:
            self.filename = "selvaDB"+str(randint(1000,9999))+".txt"
        else:
            self.filename = fileName
        if self.filename in self.filesUsed:
            raise Exception("Error: This file is already used by some other process")
        self.filesUsed.append(self.filename)

        # try:
        #     open(self.filename).close()
        # except IOError:
        #     open(self.filename,"w").close()

        '''Global file handler for all operations'''
        self.fileHandler = open(self.filename, 'wb+')


    def writeFile(self, data):
        '''
        Method to write data(json) into file
            -> check file size - if it exceeds 1GB throw exception
            -> file is not empty - delete last char(}) from file, write ,
            -> move file pointer to end
            -> write data
        '''
        file_size = os.path.getsize(self.filename)/(1024*1024)
        if(file_size>1024):
            raise Exception("Error: File size should be less than or equal to 1GB")
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
        '''
        Read data from file
           -> entire file will have json data, in this every key, value is inserted data
           -> retrieve entire data, and load it as json      
        '''
        self.fileHandler.seek(0, 0)
        read_data = self.fileHandler.readline()
        return json.loads(read_data)

    def delLastFile(self,):
        '''
        Delete Last char from file
            ->move file pointer to end
            ->truncate char    
        '''
        with open(self.filename, 'rb+') as tempFileHandle:
            tempFileHandle.seek(-1, os.SEEK_END)
            tempFileHandle.truncate()
            tempFileHandle.close()

    def commit(self,deleteList):
        '''
       Delete keys from file
           ->usually delete operation is less as compared to add and get
           ->this commit is similar to traditional sql commit, ideally this method should be invoked
               1. when exceeds buffer size
               2. after some reads and writes
               3. before closing db connection
           ->this reduces file read write calls (system call)
           -> instead of deleting every key, and performing read write is better than
              cumulatively deleting keys and performing single write
        '''
        if len(deleteList) > 0:
            data = self.readFile()
            for key in deleteList:
                if key in data.keys():
                    del data[key]
            with open(self.filename, "w") as f:
                f.close()
            self.writeFile(data)
            return True
        return False