#!/bin/bash

# Invokes Luke Lucene GUI application

DIR=$(pwd -P)
EXEC="java -jar ${DIR}/luke*.jar"

$($EXEC)
