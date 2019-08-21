#!/bin/bash

log() {
  echo "`date +%Y-%M-%d` - $1"
}

DIR=$(pwd -P)
INDEX_DB=lucene_db
JSON_INPUT=data

if [ -d $DIR/$INDEX ];
then
log "Removing old index..."
rm -r $DIR/$INDEX_DB
log "... old index removed!"
fi

if [ -f $DIR/all.csv ];
then
log "Removing old CSV..."
rm $DIR/all.csv
log "... old CSV removed!"
fi

log "Creating new index"
$DIR/index.py $INDEX_DB $JSON_INPUT
log "All done! Bye."
exit 0
