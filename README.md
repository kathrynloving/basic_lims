<h2>
Upload and display assay data in a web app
</h2>

This is meant to run locally, inside your network.
This shows how to use .csv files as the backend "database".
This is not recommended as a long-term or ideal solution, just a proof of concept that this is possible!

Set up a Python virtual environment and then launch the app:
virtualenv venv
pip install -r requirements.txt
python ./app.py 

A subset of the BindingDB data is included by default.

Try uploading new_data.csv and viewing again to see the new data!

10000 compounds is about the limit of what you'd want to view
using a .csv backend like this. 
If you upload bindingDB_purchase_target_10000.tsv the app will take about 30 seconds to load.

