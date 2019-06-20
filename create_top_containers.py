import requests
import json
import csv
from datetime import datetime

# This script will create a new container and link it as an instance to an existing accession/resource
# This was written under the assumption that you might have a csv (or similar) with an existing accession/resource uri
# The uri is used by the ASpace API to create the top container, lookup the associated accession/resource, store it's JSON,
# and create an instance in that accession/resource for the new container and repost the accession/resource to ASpace.
# There is an optional portion of the top_container json to also associate it to a location

# The barcode_csv will be your starting csv with the barcode of the container, the container number (e.g. '1' for Box 1),
# and the uri of the accession/resource to be updated, and, optionally, the uri of an archivesspace location.

barcode_csv = raw_input('name of container file: ')

# Modify your ArchivesSpace backend url, username, and password as necessary
aspace_url = 'aspace_url'
username= 'username'
password = 'password'
repo_num = '2'

auth = requests.post(aspace_url+'/users/'+username+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session':session}

with open(barcode_csv,'rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
		# Mapping the csv file to variables for the script
        barcode = row[0]
        indicator = row[1]
        # Grab the accessions URI from the csv
        ref_id = row[2]
        location_ref = row[3] 
	#comment out location_ref if no location in csv
        accession_json = requests.get(aspace_url+ref_id,headers=headers).json()

		#Start building the values for the new top container
        display_string = 'Box '+indicator+': ['+barcode+']'
        long_display = ' Box '+indicator+': ['+barcode+']'
        start_date = datetime.now().isoformat().split("T")[0]
        # Form the container JSON - if not adding locations you can remove the container_locations portion at the end
        top_container = {'barcode':barcode,'indicator':indicator,'created_for_collection':ref_id,'type':'box','jsonmodel_type':'top_container','collection':[{'ref':ref_id}],'repository':{'ref':'/repositories/2'},'display_string':display_string,'long_display_string':long_display,'container_locations':[{'jsonmodel_type': 'container_location', 'status':'current', 'start_date': start_date, 'ref':location_ref}]}
        top_container_data = json.dumps(top_container)

        # Post the top container
        top_container_post = requests.post(aspace_url+'/repositories/2/top_containers',headers=headers,data=top_container_data).json()
            
		# Grab the new container's uri
        top_container_uri = top_container_post['uri']
        print 'Top Container created:', top_container_uri       

        # Build a new instance to add to the accession/resource object, linking to the new container
        acc_instance = {'instance_type':'mixed_materials', 'sub_container':{'jsonmodel_type':'sub_container','top_container':{'ref':top_container_uri}}}
	#default is mixed_materials, but it's possible to add an additional column in the input csv

        # Append the new instance to the existing accession record's instances
        accession_json['instances'].append(acc_instance)
        acc_data = json.dumps(accession_json)

        # Repost the accession
        acc_update = requests.post(aspace_url+ref_id,headers=headers,data=acc_data).json()

        print acc_update
