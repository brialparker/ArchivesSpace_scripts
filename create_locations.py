import requests
import json

#update with correct username/password
aspace_url = 'http://localhost:8089'
username = 'username'
password = 'password'

#authentication/session information
auth = requests.post(aspace_url+'/users/'+username+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session':session, 'Content_Type':'application/json'}

#post locations
jsonfile = open('locations.json') #update filename
jsonfile = json.load(jsonfile)
for line in jsonfile:
		locationPost = json.dumps(line)
		post = requests.post(aspace_url+'/locations', headers=headers, data=locationPost).json()
		print post
