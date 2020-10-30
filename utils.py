# utils.py

def readFile(fileName):
    fh = open(fileName, mode="r")
    content = fh.read()
    fh.close()
    return content