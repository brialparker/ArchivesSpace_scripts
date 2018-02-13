import requests
import json
import csv

#the following will take a csv input containing a digital object URI, a persistent URL (in my case a handle link), and a unique id of an image
#to create a file version in a digital object that uses the IIIF API to make a thumbnail, make that thumbnail clickable, and link out to the persistent URL
image_csv = 'aspace_do_update_test.csv'

# Modify your ArchivesSpace backend url, username, password, repo_num as necessary. I know there is another way to do this using secrets, but I haven't done that yet.
aspace_url = 'your url here'
username = 'username'
password = 'password'
repo_num = '2'

auth = requests.post(aspace_url+'/users/'+username+'/login?password='+password).json()
session = auth['session']
headers = {'X-ArchivesSpace-Session':session}

with open(image_csv,'rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:

        do_id = row[0]
        handle = row[1]
        image_pid = row[2]
        do_uri = aspace_url+'/repositories/'+repo_num+'/digital_objects/'+do_id
        do_json = requests.get(do_uri,headers=headers).json()
        do_json['file_versions'][0]['file_uri'] = 'https://your.iiif.url/images/fedora2:'+image_pid+'/full/200,/0/default.jpg'
        #can adjust thumbnail size (e.g. 200,) to suit your needs
        do_json['file_versions'][0]['xlink_show_attribute'] = 'embed' #I think this is the thing that makes the thumbnail clickable
        new_file_version = {'file_uri':handle, 'jsonmodel_type':'file_version', 'published':True}
        do_json['file_versions'].append(new_file_version)
         #the above two lines create the file version that has the link you want opened when the thumbnail is clicked
        do_update = requests.post(do_uri,headers=headers,data=json.dumps(do_json))
        print str(do_uri) + ' updated!'

