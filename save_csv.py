import pandas as pd 
import numpy as np 
import os 
import json 
import yaml
import re 

def extract_components(filename):
    # filename without "_results.json"
    name = filename.replace('_results.json', '')
    pattern = r'^j(\d+)_r([\d.]+)_E(.*?)_m(\d+)$'
    match = re.match(pattern, name)
    if match:
        return match.groups()  # returns tuple (J, R, E, M)
    return None

if __name__ == '__main__':
    # Load config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    cwd = os.getcwd()
    print("Current Working Directory:", cwd)
    data_dir = f"{cwd}/pysubebm/test/my_data"
    data_files = os.listdir(data_dir) 

    all_results = []
    for data_file in data_files:
        fname = data_file.replace('.csv', '')
        J, R, E, M = extract_components(fname)
        curr_result = {
            'J': J, 
            'R': R,
            'E': E, 
            'M': M
        }
        sustain_res = os.path.join(config['SUSTAIN_FOLDER'], f"{fname}_results.json")
        my_res = os.path.join(config['MY_FOLDER'], f"{fname}_results.json")
        with open(sustain_res, 'r') as f:
            sustain_data = json.load(f)
        with open(my_res, 'r') as f:
            subebm_data = json.load(f)
        curr_result['subebm_tau'] = subebm_data['kendalls_tau']
        curr_result['subebm_subtype_acc'] = subebm_data['subtype_assignment_accuracy']
        curr_result['n_subtypes'] = subebm_data['n_subtypes']
        curr_result['sustain_tau'] = sustain_data['tau']
        curr_result['sustain_subtype_acc'] = sustain_data['subtype_acc']
        all_results.append(curr_result)
    
    df = pd.DataFrame(all_results)
    print('SUBEBM TAU AVG:', df['subebm_tau'].mean())
    print('SUBEBM SUBTYPE ACC AVG:', df['subebm_subtype_acc'].mean())
    print('SUSTAIN TAU AVG:', df['sustain_tau'].mean())
    print('SUSTAIN SUBTYPE ACC AVG:', df['sustain_subtype_acc'].mean())
    df.to_csv('all_results.csv', index=False)

        

    

