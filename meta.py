import os
import sys
from stat import *

def main():
	fileData = raw_input()
	data = os.stat(fileData)
	print(data[ST_INO])
	print(str(data[ST_UID])
	print(data[ST_SIZE])
	print(data[ST_ATIME])
	print(data[ST_MTIME])
	print(data[ST_CTIME])
	

if __name__ == "__main__": 
	main()
