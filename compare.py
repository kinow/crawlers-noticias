#!/usr/bin/env python

# system, IO and logging
import sys
from os import listdir
from os.path import isfile, join
import logging
# create logger
logger = logging.getLogger('compare_news')
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
from lucene import SimpleFSDirectory, File, Document, Field, \
    KeywordAnalyzer, IndexSearcher, Version, QueryParser

# JSON
import json

# NLTK
import nltk

# Lucene Max Hits per search
MAX_HITS = 10000

def main(indexDir, inputDir):
    """Creates a SQLite database with news linked to other news by at least one term, backed by a Lucene Index"""
    lucene.initVM()

    # Open index
    logger.info("Opening Lucene index [%s]..." % indexDir)
    dir = SimpleFSDirectory(File(indexDir))
    analyzer = KeywordAnalyzer(Version.LUCENE_CURRENT)
    searcher = IndexSearcher(dir)

    # Search documents
    onlyfiles = [ f for f in listdir(inputDir) if isfile(join(inputDir, f)) and f.endswith('.json') ]
    for f in onlyfiles:
        json_data = open(inputDir + '/' + f)
        data = json.load(json_data)
        # The results collected after comparison
        results = list();

        journal_code = f.split('.')[0]

        for entry in data:
            url = entry['url']
            date = entry['date']
            title = entry['title']

            logger.debug("Processing URL [%s] date [%s] - [%s]" % (url, date, title))

            tt = nltk.word_tokenize(title)
            tokens = []
            for t in tt:
                tokens.append(t.lower())

            entry['similars'] = list()

            for token in tokens:
                q = 'title: "%s" AND date: "%s" AND NOT journal: "%s" AND NOT url: "%s"' % (token, date, journal_code, url)
                query = QueryParser(Version.LUCENE_CURRENT, "title", analyzer).parse(q)
                hits = searcher.search(query, MAX_HITS)

                logger.debug("Found %d document(s) that matched query '%s':" % (hits.totalHits, q))

                for hit in hits.scoreDocs:
                    doc = searcher.doc(hit.doc)
                    logger.debug(doc)
                    entry['similars'].append({'token': token, 'url': doc.get('url'), 'title': doc.get('title')})

            results.append(entry)
        json_data.close()

        print """<html>
    <body>
    <table><thead>
    <tr>
    <th>Jornal</th><th>Data</th><th>T&iacute;tulo</th><th>URL</th><th>Not&iacute;cias semelhantes</th>
    </tr>
    </thead>
    <tbody>
    """
        for entry in results:
            similars = entry['similars']
            similars_text = '<ul>'
            for s in similars:
                similars_text += '<li>[%s] [%s] [%s]</li>' % (s['token'].encode('iso-8859-1', 'ignore'), s['title'].encode('iso-8859-1', 'ignore'), s['url'].encode('iso-8859-1', 'ignore'))
            similars_text += '</ul>'
            print """<tr>
    <td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>
    </tr>
    """ % (journal_code, entry['date'].encode('iso-8859-1', 'ignore'), entry['title'].encode('iso-8859-1', 'ignore'), entry['url'].encode('iso-8859-1', 'ignore'), similars_text)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Usage: compare.py <index_dir> <input_dir>'
        sys.exit(2)
    indexDir = sys.argv[1]
    inputDir = sys.argv[2]
    main(indexDir, inputDir)
