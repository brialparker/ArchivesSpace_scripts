#!/bin/bash

for line in $(cat lit_ids2.json); do
	uri = $(jq .'uri' <<<"$line" | sed 's/\"//g')

#be sure to replace with filename of json file 

	echo $uri
#	echo `curl -H "X-ArchivesSpace-Session: $TOKEN" -d $line "http://aspacestage.lib.umd.edu:8089$uri"`;
done


#cat lit_accessions.json | jq .[] | jq ."uri" | sed 's/\"//g'