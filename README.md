# ArchivesSpace_scripts for University of Maryland Special Collections and University Archives
Some scripts developed to work with ArchivesSpace API, mostly hacked from something else I found, because you people are generous
and kind and share your work for others like me to learn from. 

**aspace_image_thumbnails.py**
Takes a csv file with digital object URIs, handles (or other persistent URL) and IIIF ids and updates existing digital objects 
with a IIIF thumbnail image that links to the handle when clicked.

**create_locations.py**  
Takes a json file of location data (see aspace_sample_locations.json) and posts new location objects to ArchivesSpace
Note: I could not use the batch location creation native to ArchivesSpace, based on the numbering and how the feature treated numbers.
It was all very weird, so this was my workaround. 
Another note: I created the json from a csv that I loaded into OpenRefine and used the templating tool to create the json.

**create_top_containers.py**
Takes a csv of barcodes, box numbers, accession or resource uris, and location uris, and creates top containers, 
associating them to the accession/resource and location in csv.

**get_linked_agents.py**
Retrieves records that are linked to a specific agent. Then, retrieves uris and names of ALL the agents linked 
to the returned resources. I inted to use this locally for quality control, as we associate new resources/accessions with 
a dummy agent to trigger a review for authorities (since aspace has done some weird stuff on import with duplicates, etc.)

**resource_type_update.py**
This is my attempt to assign resource types to imported resources by checking for terms in the resource title.
