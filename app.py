from flask import *
import pandas as pd
app = Flask(__name__)

# If you have many datasets, you may want your index.html at
# route "/" to link to each, where /bindingdb is just one...
# But in this simple example, bindingdb is all you get!
@app.route("/")
@app.route("/bindingdb")
def show_tables():
    data_path = 'bindingDB_purchase_target_subset.tsv'
    header = ['target_name', 'uniprot_id', 'smiles', 'bindingdb_id', 'affinity_type', 'affinity_value', 'source', 'price']
    data = pd.read_csv(data_path, sep='\t', names=header)  # for tsv file
    # data = pd.read_excel(data_path)  # for Excel file
    data.set_index(['bindingdb_id'], inplace=True)
    data.index.name=None
    ic50_data = data.loc[data.affinity_type=='IC50']
    ec50_data = data.loc[data.affinity_type=='EC50']
    return render_template('view.html',tables=[ic50_data.to_html(classes='IC50'), ec50_data.to_html(classes='EC50')],
    titles = ['na', 'IC50 data', 'EC50 data'])

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    app.run(debug=True)
