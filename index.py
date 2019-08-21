#!/usr/bin/env python

# system, IO and logging
import sys
from os import listdir
from os.path import isfile, join
import logging
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

# Lucene
import lucene
lucene.initVM(lucene.CLASSPATH)
from java.nio.file import Paths
from org.apache.lucene.index import IndexReader
from org.apache.lucene.index import IndexWriter
from org.apache.lucene.index import IndexWriterConfig
from org.apache.lucene.document import Document, IndexableField, FieldType
from org.apache.lucene.analysis import CharArraySet
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.store import SimpleFSDirectory

# JSON
import json

# CSV
import csv

def main(indexDir, inputDir):
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
    logger.info("Creating Lucene index [%s]..." % indexDir)

    dir = SimpleFSDirectory(Paths.get(indexDir))
    analyzer = StandardAnalyzer(stopwords)
    writerConfig = IndexWriterConfig(analyzer)
    writer = IndexWriter(dir, writerConfig)

    logger.info("Currently there are %d documents in the index..." % writer.numDocs())

    # Index documents
    onlyfiles = [ f for f in listdir(inputDir) if isfile(join(inputDir, f)) and f.endswith('.json') ]
    for f in onlyfiles:
        try:
            journal_code = f.split('.')[0]
            f = join(inputDir, f)
            json_data = open(f)
            data = json.load(json_data)
            for entry in data:
                doc = Document()
                doc.add(Field("journal", journal_code, Field.Store.YES, Field.Index.NOT_ANALYZED))
                doc.add(Field("url", entry['url'], Field.Store.YES, Field.Index.NOT_ANALYZED ))
                doc.add(Field("date", entry['date'], Field.Store.YES, Field.Index.NOT_ANALYZED ))
                doc.add(Field("title", entry['title'], Field.Store.YES, Field.Index.ANALYZED))
                writer.addDocument(doc)
            json_data.close()
        except (IOError) as v:
            try:
                (code, message) = v
            except:
                code = 0
                message = v
            logger.error("I/O Error: " + str(message) + " (" + str(code) + ")")
    logger.info("Indexed lines from stdin (%d documents in index)" % writer.numDocs())

    # Wrap it up
    #logger.info("About to optimize index of %d documents..." % writer.numDocs())
    #writer.optimize()
    #logger.info("...done optimizing index of %d documents" % writer.numDocs())

    logger.info("Closing index of %d documents..." % writer.numDocs())
    writer.close()

    reader = IndexReader.open(dir)
    with open('all.csv', 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        for i in range(0, reader.numDocs()):
            doc = reader.document(i)
            csvwriter.writerow([doc.get('journal'), doc.get('date'), doc.get('url').encode('utf8'), \
                doc.get('title').strip().replace(',', '\,').encode('utf8')])

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: index.py <index_dir> <input_dir>')
        sys.exit(2)
    #indexDir = "/tmp/REMOVEME.index-dir"
    #inputDir = '.'
    indexDir = sys.argv[1]
    inputDir = sys.argv[2]
    main(indexDir, inputDir)
