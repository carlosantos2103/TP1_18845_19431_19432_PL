# utils.py

def readFile(file_name):
    fh = open(file_name, mode="r")
    content = fh.read()
    fh.close()
    return content


def clearFile(file_name):
    open(file_name, 'w').close()


def writeFile(file_name, content):
    with open(file_name, mode="a") as fh:
        fh.write(content)
    fh.close()
    pass
