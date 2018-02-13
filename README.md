# ArchivesSpace_scripts
some scripts developed to work with ArchivesSpace API

**aspace_image_thumbnails.py**
Takes a csv file with digital object URIs, handles (or other persistent URL) and IIIF ids and updates existing digital objects 
with a IIIF thumbnail image that links to the handle when clicked.

**create_locations.py**  
Takes a json file of location data (see aspace_sample_locations.json) and posts new location objects to ArchivesSpace

**create_top_containers.py**
Takes a csv of barcodes, box numbers, accession or resource uris, and location uris, and creates top containers, 
associating them to the accession/resource and location in csv.
