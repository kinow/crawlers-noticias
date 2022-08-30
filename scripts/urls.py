#!/usr/bin/env python
import sys
import json
import datetime

reload(sys)
sys.setdefaultencoding('iso-8859-1')

"""Fix SBT news' URL's."""


def main():
	  with open('sbt.json', 'r') as f:
	      data = json.load(f)
	      new_data = []
	      for entry in data:
            url = entry['url'].replace("http:/", 'http://')
    		    entry['url'] = url
    		    new_data.append(entry)

	  with open('sbt2.json', 'w+') as f:
	      json.dump(new_data, f)


if __name__ == '__main__':
    main()
