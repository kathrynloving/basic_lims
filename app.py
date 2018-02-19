import os
import sys
import glob
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request, redirect, flash, url_for
from flask import send_from_directory, render_template
import pandas as pd
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "./uploads"  # better to move this elsewhere on your server
ALLOWED_EXTENSIONS = set(['tsv', 'csv'])  # consider adding txt, xlsx, ...

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    """
    Try to prevent users from uploading bad files.
    The "secure_filename" function is meant to help as well.
    """
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# This is the route to the top level of your app.
# If you have many datasets, you may want your index.html at
# route "/" to have a link to each dataset, and maybe other info.
# But in this simple example, bindingdb is the only data type available.
@app.route("/")
@app.route("/bindingdb")
def show_tables():
    """
    Load all available data files that have the right format.
    All files will be assumed to have the same 8 fields in the header.
    This demonstrates pulling a specific file name as well as
    wildcard file search in the uploads/ directory.
    And as an example, filtering the data to only show relevant
    (IC50 and EC50) rows in the app.
    """
    header_format = ['target_name', 'uniprot_id', 'smiles', 'bindingdb_id',
                     'affinity_type', 'affinity_value', 'source', 'price']
    list_of_data = []
    data_path = 'bindingDB_purchase_target_subset.tsv'
    data = pd.read_csv(data_path, sep='\t', names=header_format, header=0)  # for tsv file
    # data = pd.read_excel(data_path)  # for Excel file
    data.set_index(['bindingdb_id'], inplace=True)
    list_of_data.append(data)
    uploaded_files = glob.glob(os.path.join(app.config['UPLOAD_FOLDER'],
                                            "*.csv"))
    app.logger.warning("Loading files:")
    app.logger.warning(os.path.join(app.config['UPLOAD_FOLDER'],"*.csv"))
    app.logger.warning(uploaded_files)
    for upload_file in uploaded_files:
        app.logger.warning("Loading uploaded file %s" % upload_file)
        data = pd.read_csv(upload_file, names=header_format, header=0)  # for csv file
        data.set_index(['bindingdb_id'], inplace=True)
        list_of_data.append(data)
    df = pd.concat(list_of_data)
    df.index.name = None
    ic50_data = df.loc[df['affinity_type'].str.contains("IC50")]
    ec50_data = df.loc[df['affinity_type'].str.contains("EC50")]
    return render_template('view.html',
                           tables=[ic50_data.to_html(classes='IC50'),
                                   ec50_data.to_html(classes='EC50')],
                           titles=['na', 'IC50 data', 'EC50 data'])

# Allow uploading new data for display
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('show_tables'))

    return '''
    <!doctype html>
    <title>Upload new file of data in bindingDB format</title>
    <h1>Upload new file of compound data in bindingDB format</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

# Adding a blank favicon because it is required.
# Change to your own favorite favicon image if you like!
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


if __name__ == "__main__":
    handler = RotatingFileHandler('basic_lims_app.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(debug=True)
