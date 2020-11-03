# utils.py

def readFile(file_name):
    fh = open(file_name, mode="r")
    content = fh.read()
    fh.close()
    return content
