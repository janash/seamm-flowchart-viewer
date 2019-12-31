import os

from flask import Flask, render_template, request, session, redirect, url_for, flash
from werkzeug.utils import secure_filename

from util import process_flowchart, allowed_file

app = Flask(__name__)
app.secret_key = b'i\xe4\xdbKG0\xe7\xb8\x90\xd3]\x0foI\x12\x85'

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'flowcharts', 'temp')
ALLOWED_EXTENSIONS = set(['flow'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=['GET', 'POST'])
def home():
    session['flowchart'] = os.path.join('flowcharts', 'demos', 'hc_mopac.flow')
    return render_template('home.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
            
            if not os.path.exists(UPLOAD_FOLDER):
                os.mkdir(UPLOAD_FOLDER)

            filename = secure_filename(file.filename)

            filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filename)
            
            session['flowchart'] = filename

            return redirect(url_for('draw_flowchart'))
    return render_template("upload.html")

@app.route('/view_flowchart', methods=['GET', 'POST'])
def draw_flowchart():

    sample_flow = session['flowchart']
    important_stuff = process_flowchart(sample_flow)['flowchart_json']


    # Process the flowchart
    elements = []

    for node in important_stuff['nodes']:
        #print(node)
        elements.append({'data': {
            'id': node['attributes']['_uuid'],
            'name': node['attributes']['_title'],
            
        },
        'position': {
                "x": node['attributes']['x'],
                "y": node['attributes']['y']
            },

        'description': "",                
        })
        
        keys = [key for key in node.keys() if 'flowchart' in key.lower() ]
        

    for edge in important_stuff['edges']:
        node1_id = edge['node1']
        node2_id = edge['node2']
        edge_data = {'data':
            {
                'id': str(node1_id) + '_' + str(node2_id),
                'source': node1_id, 
                'target': node2_id
            },
            
        }

        elements.append(edge_data)


    return render_template('render_flowchart.html', data=elements)

if __name__ == "__main__":
    
    
    app.run(debug=True)
