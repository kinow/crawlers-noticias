#!/usr/bin/env python

import sys
import json
import datetime

def main():
	# JN date format is not right
	f = open('jn.json', 'r')
	data = json.load(f)
	new_data = []
	for entry in data:
		date = datetime.datetime.strptime(entry['date'], '%Y/%m/%d')
		entry['date'] = str(date)
		new_data.append(entry)
	f.close()

	f = open('jn2.json', 'w+')
	json.dump(new_data, f)
	f.close()

if __name__ == '__main__':
    main()