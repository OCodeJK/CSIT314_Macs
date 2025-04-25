# Before Running:
 pip install -r requirements.txt to install all relevant dependencies
 
 
 # To Run:
 python main.py to run the app
 localhost:5000 to access it
 


# Database:
To ensure you are using the latest database do:

pg_restore -U username -d c2c_db < db.dump

OR

psql -U username c2c_db db.dump



# Folder/File structures:

boundary: Contains all the boundary related file

control: Contains all the controller related file

entity: Contains all the entity related file

template: contains all the html files to be rendered (CSS included)

helper: contains extra functions to help with the program (for neatness)
