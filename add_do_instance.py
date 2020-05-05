import requests
import json
import csv
import os

# Starting with an input CSV, this script will use the ArchivesSpace API to batch create digital object records in ASpace 
# as an instance of specified archival object parent (e.g. a series/subseries/file).

#AUTHENTICATION STUFF:

aspace_url = 'http://localhost:8089'
username = 'admin'
password = 'admin'

repo_num = raw_input('Enter repository number: ')
archival_object_csv = raw_input('Enter csv file of digital objects to be added: ')

auth = requests.post(aspace_url+'/users/'+username+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session':session}

#Open Input CSV and iterate over rows
with open(archival_object_csv,'rb') as csvfile:
    csvin = csv.reader(csvfile)
    next(csvin, None) #ignore header row
    for row in csvin:

#ARCHIVAL OBJECT STUFF

        ao_id = row[0]           
        do_id = row[5] #this is usually the filename prefix, ie. litms-012345
        do_iiif = row[2] #this is usually the pid from fedora2
        handle = row[3]

        iiif = 'https://iiif.lib.umd.edu/images/fedora2:'+do_iiif+'/full/200,/0/default.jpg'
     #  example iiif thumbnail url: https://iiif.lib.umd.edu/images/fedora2:umd:723225/full/200,/0/default.jpg
        archival_object_json = requests.get(aspace_url+ao_id,headers=headers).json()

        display_string = archival_object_json['display_string']
        #build the digital object json object
        dig_obj = {'title':display_string, 'publish':True,'digital_object_id':do_id,'digital_object_type':'still_image','file_versions':[{'file_uri':iiif,'jsonmodel_type':'file_version', 'publish':True,'xlink_show_attribute':'embed'},{'file_uri':handle, 'jsonmodel_type':'file_version', 'publish':True}]}
        #if digital objects are A/V materials comment out the above line and uncomment the below line, taking care to adjust digital_object_type
        #dig_obj = {'title':display_string, 'publish':True,'digital_object_id':do_id,'digital_object_type':'audio','file_versions':[{'file_uri':handle, 'jsonmodel_type':'file_version', 'publish':True}]}

        dig_obj_data = json.dumps(dig_obj)
        #post the new digital object back to ArchivesSpace
        dig_obj_post = requests.post(aspace_url+'/repositories/'+repo_num+'/digital_objects',headers=headers,data=dig_obj_data).json()

        # Grab the new digital object uri
        dig_obj_uri = dig_obj_post.get('uri')

        print 'New DO URI: ' + str(dig_obj_uri)

         # Build a new instance to add to the archival object, linking to the digital object
        dig_obj_instance = {'instance_type':'digital_object', 'digital_object':{'ref':dig_obj_uri}}

         # Append the new instance to the existing archival object record's instances and post to ArchivesSpace
        archival_object_json['instances'].append(dig_obj_instance)
        archival_object_data = json.dumps(archival_object_json)
        archival_object_update = requests.post(aspace_url+ao_id,headers=headers,data=archival_object_data).json()
        print 'New DO added as instance of new AO: ', archival_object_update.get('uri')
