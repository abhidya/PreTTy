import os
import sys, time
from stat import *

def main():
    fileData = input("Enter file: ")
    data = os.stat(fileData)
    test = data[ST_INO]
    print("ST_INO "+str(data[ST_INO]))
    print("ST_DEV "+str(data[ST_DEV]))
    print("ST_UID "+str(data[ST_UID]))
    print("ST_SIZE "+str(data[ST_SIZE]))
    print(time.asctime(time.localtime(data[ST_ATIME])))
    print(time.asctime(time.localtime(data[ST_MTIME])))
    print(time.asctime(time.localtime(data[ST_CTIME])))
	

if __name__ == "__main__": 
	main()
