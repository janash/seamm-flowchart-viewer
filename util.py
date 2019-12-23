import os
import json
import hashlib

def process_flowchart(flowchart_path):
    """Read in flowchart from file and process for addition to SEAMM datastore.

    Parameters
    ----------
        flowchart_path: str
            The location of the flowchart
    
    Returns
    -------
        flowchart_info: dict
            Dictionary of flowchart information.
    """
    flowchart_info = {}

    flowchart_info['path'] = os.path.abspath(flowchart_path)

    # Get the flowchart text
    with open(flowchart_path, 'r') as f:
        flowchart_info['flowchart_file'] = f.read()
    
    # Get the flowchart description
    with open(flowchart_path) as f:
        f.readline()
        f.readline()
        flowchart_info['flowchart_json'] = json.load(f)

    # Get a hash of the flowchart contents
    flowchart_info['id'] = hashlib.md5(flowchart_info['flowchart_file'].encode('utf-8')).hexdigest()

    # Get the flowchart description.
    flowchart_info['description'] = flowchart_info['flowchart_json']['nodes'][0]["attributes"]['_description']

    return flowchart_info

def allowed_file(filename, ALLOWED_EXTENSIONS):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
