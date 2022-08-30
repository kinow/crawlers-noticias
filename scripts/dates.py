#!/usr/bin/env python

import sys
import json
import datetime

def main():
	# JN date format is not right
	with open('jn.json', 'r') as f:
    data = json.load(f)
    new_data = []
    for entry in data:
      date = datetime.datetime.strptime(entry['date'], '%Y/%m/%d')
      entry['date'] = str(date)
      new_data.append(entry)

	with open('jn2.json', 'w+') as f:
	  json.dump(new_data, f)

if __name__ == '__main__':
    main()
