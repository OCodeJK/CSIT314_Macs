# Before Running:
 pip install -r requirements.txt to install all relevant dependencies
 
 
 # To Run:
 - python main.py to run the app
 - localhost:5000 to access it
 


# Database Restoration:
To ensure you are using the latest database do:

pg_restore -U username -d database_name < db.dump

OR

psql -U username -d database_name -f dump.sql

# Dumping Database:
To ensure we can keep our database updated do:

pg_dump -U username -Fc mydbname > db.dump

OR

pg_dump -U username mydbname > db.sql

# Folder/File structures:

boundary: Contains all the boundary related file

control: Contains all the controller related file

entity: Contains all the entity related file

template: contains all the html files to be rendered

static: contains all the relevant css files for our templates

helper: contains extra functions to help with the program (for neatness)
