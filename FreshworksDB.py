import json
filename = 'filename.txt'


def writeFile(data):
    writerFile = open(filename, 'wb')
    writerFile.write(json.dumps(data).encode())
    writerFile.close()


def readFile():
    readrFile = open(filename, 'rb')
    read_data = readrFile.readline()
    return json.loads(read_data)


writeFile({'Starspy': 1, 'bfvjbvf': 'Test1'})
print(readFile())
writeFile({'Starspy': 2, 'bfvjbvf': 'Test1'})
print(readFile())
