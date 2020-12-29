import json
import os
filename = 'filename.txt'

fileHandler = open(filename, 'wb+')


def writeFile(data):
    global fileHandler
    try:
        delLast()
        da = json.dumps(data)
        res = ', '+da[1:]
        print(res)
        fileHandler.write(res)
    except:
        print("out")
        fileHandler.write(json.dumps(data).encode())
    fileHandler.flush()


def readFile():
    global fileHandler
    fileHandler.seek(0, 0)
    read_data = fileHandler.readline()
    # return read_data
    # fileHandler.flush()
    return json.loads(read_data)

# {"Starspy": 1, "bfvjbvf": "Test1", "mani": 1, "fhb": "Test1"}


def delLast():
    with open(filename, 'rb+') as filehandle:
        filehandle.seek(-1, os.SEEK_END)
        filehandle.truncate()
        # filehandle.write(' ')
        filehandle.flush()
        filehandle.close()


def pp():
    with open(filename, 'r+') as filehandle:
        da = filehandle.readline()
        # print(da)
        print(json.loads(da))
        # print(da)
        filehandle.close()


writeFile({'Starspy': 1, 'bfvjbvf': 'Test1', 'sia': 'jkfvb'})
# writeFile({'Starspy': 2, 'bfvjbvf': 'Test1'})
delLast()
# print(pp())


data = {'mani': 1, 'fhb': 'Test1'}
fileHandler.seek(0, os.SEEK_END)
da = json.dumps(data)
res = (', '+da[1:]).encode()
print(res)
fileHandler.write(res)
fileHandler.flush()
print(pp())
# print(pp())

# # delLast()
# writeFile({'mani': 1, 'fhb': 'Test1'})
# # # # # writeFile({'mani': 1, 'bfvjbvf': 'Test1'})
# print(pp())
# # fileHandler.close()


# # print(readFile())
# # print(readFile())
# # print(readFile())
# # delLast()
# # print(readFile())
