#!/bin/bash

log() {
  echo "`date +%Y-%M-%d` - $1"
}

DIR=$(pwd -P)
INDEX_DB=lucene_db
JSON_INPUT=data

if [ -f $DIR/relationships.csv ];
then
log "Removing old CSV..."
rm $DIR/relationships.csv
log "... old CSV removed!"
fi

log "Creating relationships CSV"
$DIR/relationships.py $INDEX_DB $JSON_INPUT
log "All done! Bye."
exit 0
