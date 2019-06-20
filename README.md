# ArchivesSpace scripts for University of Maryland Special Collections and University Archives
Some scripts developed to work with ArchivesSpace API, mostly hacked from something else I found, because you people are generous
and kind and share your work for others like me to learn from. 

**aspace_image_thumbnails.py**
Takes a csv file with digital object URIs, handles (or other persistent URL) and IIIF ids and updates existing digital objects 
with a IIIF thumbnail image that links to the handle when clicked.

**create_top_containers.py**
Takes a csv of barcodes, box numbers, accession or resource uris, and location uris, and creates top containers, 
associating them to the accession/resource and location in csv.

**get_linked_agents.py**
Retrieves records that are linked to a specific agent. Then, retrieves uris and names of ALL the agents linked 
to the returned resources. I intend to use this locally for quality control, as we associate new resources/accessions with 
a dummy agent to trigger a review for authorities (since aspace has done some weird stuff on import with duplicates, etc.)

**new_accessions.py**
Retrieves accessions created over the past month for review/reporting by one of our collection managers, using [ArchivesSnake](https://github.com/archivesspace-labs/ArchivesSnake). The script Uses authorization yml file described [here](https://github.com/archivesspace-labs/ArchivesSnake#configuration).

**resource_type_update.py**
This is my attempt to assign resource types to imported resources by checking for terms in the resource title.
