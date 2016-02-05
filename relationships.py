#!/usr/bin/env python

# system, IO and logging
import sys
from os import listdir
from os.path import isfile, join
import logging
# create logger
logger = logging.getLogger('compare_news')
logger.setLevel(logging.INFO)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)

# Lucene
import lucene
lucene.initVM(lucene.CLASSPATH)
from java.io import File
from org.apache.lucene.document import Document, Field
from org.apache.lucene.util import Version
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.analysis.core import KeywordAnalyzer

# JSON
import json

# NLTK
import nltk
nltk.data.path.append("/home/kinow/Development/python/nltk_data")

# CSV
import csv

# Lucene Max Hits per search
MAX_HITS = 10000

def main(indexDir, inputDir):
	"""Creates a SQLite database with news linked to other news by at least one term, backed by a Lucene Index"""
	lucene.initVM()

	# Open index
	logger.info("Opening Lucene index [%s]..." % indexDir)
	dir = SimpleFSDirectory(File(indexDir))
	analyzer = KeywordAnalyzer(Version.LUCENE_CURRENT)
	reader = DirectoryReader.open(dir)
	searcher = IndexSearcher(reader)

	# Search documents
	onlyfiles = [ f for f in listdir(inputDir) if isfile(join(inputDir, f)) and f.endswith('.json') ]
	rels = list()
	for f in onlyfiles:
		journal_code = f.split('.')[0]
		f = join(inputDir, f)
		json_data = open(f)
		data = json.load(json_data)
		# The results collected after comparison

		for entry in data:
			url = entry['url']
			date = entry['date']
			title = entry['title']

			logger.debug("Processing URL [%s] date [%s] - [%s]" % (url, date, title))

			tt = nltk.word_tokenize(title)
			tokens = []
			for t in tt:
				tokens.append(t.lower())

			for token in tokens:
				q = 'title: "%s" AND date: "%s" AND NOT journal: "%s" AND NOT url: "%s"' % (token, date, journal_code, url)
				query = QueryParser(Version.LUCENE_CURRENT, "title", analyzer).parse(q)
				hits = searcher.search(query, MAX_HITS)

				logger.debug("Found %d document(s) that matched query '%s':" % (hits.totalHits, q))

				for hit in hits.scoreDocs:
					doc = searcher.doc(hit.doc)
					logger.debug(doc)

					rels.append({'left': url, 'token': token, 'right': doc.get('url')})
		json_data.close()

	with open('relationships.csv', 'wb') as csvfile:
		csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
		for rel in rels:
			csvwriter.writerow([rel['left'].encode('utf8'), rel['token'].encode('utf8'), rel['right'].encode('utf8')])

if __name__ == '__main__':
	if len(sys.argv) < 3:
		print 'Usage: relationships.py <index_dir> <input_dir>'
		sys.exit(2)
	indexDir = sys.argv[1]
	inputDir = sys.argv[2]
	main(indexDir, inputDir)
