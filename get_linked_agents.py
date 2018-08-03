import json
import requests
import csv

aspace_url = 'http://localhost:8080'
username = 'admin'
password = 'admin'
repo_num = '2'

#Do your authentication thing
auth = requests.post(aspace_url+'/users/'+username+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session':session}

#set endpoints with all ids to get everything
endpoint = '/repositories/2/resources?all_ids=true'
endpoint2 = '/repositories/2/accessions?all_ids=true'

#then save all the ids
ids = requests.get(aspace_url + endpoint, headers=headers).json()
acc_ids = requests.get(aspace_url + endpoint2, headers=headers).json()


records = []
#find all resources and accessions that have linked agents
for id in ids:
    resource_uri = '/repositories/2/resources/'+str(id)
    resource_json = requests.get(aspace_url + resource_uri, headers=headers).json()
    try:
        ref = resource_json['linked_agents'][0]['ref']
        records.append(resource_json)
    except:
        continue

for acc_id in acc_ids:
    acc_uri = '/repositories/2/accessions/'+str(acc_id)
    acc_json = requests.get(aspace_url + acc_uri, headers=headers).json()
    try:
        ref = acc_json['linked_agents'][0]['ref']
        records.append(acc_json)
    except:
        continue

#open a cvs file for output
f=csv.writer(open('new_agents.csv', 'wb'))
f.writerow(['uri']+['name']+['related record'])

selected_records = []
#get all records that are linked to a specific agent
for i in range (0, len (records)):
    for j in range (0, len (records[i]['linked_agents'])):
        uri = records[i]['uri']
        title = records[i]['title']
        needs_review = records[i]['linked_agents'][j].get('ref')
        if needs_review == '/agents/software/2':
            ag_json = requests.get(aspace_url + uri, headers=headers).json()
            selected_records.append(ag_json)
 
#Now take the records found above and get any related agent and write to csv           
for i in range (0, len (selected_records)):
    for j in range (0, len (selected_records[i]['linked_agents'])):
        uri = selected_records[i]['uri']
        agents = selected_records[i]['linked_agents'][j].get('ref')
        agent_json = requests.get(aspace_url + agents, headers=headers).json()
        title = agent_json['title']
        f.writerow([agents]+[title]+[uri])
