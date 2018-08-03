import json
import csv
import datetime
from datetime import timezone
import dateutil.parser
from asnake.aspace import ASpace
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()
repos = client.get("repositories").json()
                
aspace = ASpace()
repo = aspace.repositories(2)

f=csv.writer(open('new_scua_accessions.csv','w', newline=''))

last_month = datetime.datetime.now(timezone.utc) + datetime.timedelta(-30)
for accession in repo.accessions:
    created = dateutil.parser.parse(accession.create_time)
    if created > last_month:
        id = accession.id_0+'-'+accession.id_1
        f.writerow([accession.title]+[accession.uri]+[id]+[accession.create_time])
