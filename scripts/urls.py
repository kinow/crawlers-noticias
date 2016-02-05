#!/usr/bin/env python
import sys  
reload(sys)  
sys.setdefaultencoding('iso-8859-1')
import json
import datetime

def main():
	# JN date format is not right
	f = open('sbt.json', 'r')
	data = json.load(f)
	new_data = []
	for entry in data:
		url = entry['url'].replace("http:/", 'http://')
		entry['url'] = url
		new_data.append(entry)
	f.close()

	f = open('sbt2.json', 'w+')
	json.dump(new_data, f)
	f.close()

if __name__ == '__main__':
    main()