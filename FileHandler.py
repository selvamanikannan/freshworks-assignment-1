import json
import os
from LRUCache import LRUCache
import time
from random import randint
from threading import Lock


class FileHandler:
    filesUsed = []

    def __init__(self, fileName=None):
        if fileName is None:
            self.filename = "selvaDB"+str(randint(1000,9999))+".txt"
        else:
            self.filename = fileName
        if self.filename in self.filesUsed:
            raise Exception("Error: This file is already used by some other process")
        self.filesUsed.append(self.filename)

        try:
            open(self.filename).close()
        except IOError:
            open(self.filename,"w").close()

        self.fileHandler = open(self.filename, 'rb+')


    def writeFile(self, data):
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
        self.fileHandler.seek(0, 0)
        read_data = self.fileHandler.readline()
        return json.loads(read_data)

    def delLastFile(self,):
        with open(self.filename, 'rb+') as tempFileHandle:
            tempFileHandle.seek(-1, os.SEEK_END)
            tempFileHandle.truncate()
            tempFileHandle.close()

    def commit(self,deleteList):
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


    def throwException(self, data):
        self.commit()
        raise Exception(data)