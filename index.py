#!/usr/bin/env python

import csv
import json
import logging
from os import listdir
from os.path import isfile, join

import lucene
import sys
from java.nio.file import Paths
from org.apache.lucene.analysis import CharArraySet
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, StringField
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.index import IndexWriter
from org.apache.lucene.index import IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory

# create logger
logger = logging.getLogger('index_news')
logger.setLevel(logging.DEBUG)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)

lucene.initVM(lucene.CLASSPATH)


def main(index_dir, input_dir):
    """Creates a Lucene Index, and indexes every .json file it finds.
    It utilizes a stopwords.txt to filter out stop words"""
    lucene.initVM()

    logger.info("Loading stop words from stopwords.txt")
    f = open('stopwords.txt', 'r')
    stopwords = set([])
    for line in f:
        stopwords.add(line.strip())
    f.close()
    logger.debug('Stop words: %s' % str(stopwords))
    temp = CharArraySet(1, True)

    for stopword in stopwords:
        temp.add(stopword)

    stopwords = temp

    # Create index
    logger.info("Creating Lucene index [%s]..." % index_dir)

    dir = SimpleFSDirectory(Paths.get(index_dir))
    analyzer = StandardAnalyzer(stopwords)
    writerConfig = IndexWriterConfig(analyzer)
    writer = IndexWriter(dir, writerConfig)

    logger.info("Currently there are %d documents in the index..." % writer.numDocs())

    # Index documents
    onlyfiles = [f for f in listdir(input_dir) if isfile(join(input_dir, f)) and f.endswith('.json')]
    for f in onlyfiles:
        try:
            journal_code = f.split('.')[0]
            f = join(input_dir, f)
            json_data = open(f)
            data = json.load(json_data)
            for entry in data:
                doc = Document()
                doc.add(StringField("journal", journal_code, StringField.Store.YES))
                doc.add(StringField("url", entry['url'], StringField.Store.YES))
                doc.add(StringField("date", entry['date'], StringField.Store.YES))
                doc.add(StringField("title", entry['title'], StringField.Store.YES))
                writer.addDocument(doc)
            json_data.close()
        except IOError as v:
            try:
                (code, message) = v
            except (TypeError, ValueError):
                code = 0
                message = v
            logger.error("I/O Error: " + str(message) + " (" + str(code) + ")")
    logger.info("Indexed lines from stdin (%d documents in index)" % writer.numDocs())

    # Wrap it up
    # logger.info("About to optimize index of %d documents..." % writer.numDocs())
    # writer.optimize()
    # logger.info("...done optimizing index of %d documents" % writer.numDocs())

    logger.info("Closing index of %d documents..." % writer.numDocs())
    writer.close()

    reader = DirectoryReader.open(dir)
    with open('all.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        for i in range(0, reader.numDocs()):
            doc = reader.document(i)
            csvwriter.writerow([doc.get('journal'), doc.get('date'), doc.get('url').encode('utf8'),
                                doc.get('title').strip().replace(',', '\,').encode('utf8')])


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: index.py <index_dir> <input_dir>')
        sys.exit(2)
    index_dir = sys.argv[1]
    input_dir = sys.argv[2]
    main(index_dir=index_dir, input_dir=input_dir)
