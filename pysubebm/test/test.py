from pysubebm import run_subebm
import os
import json 

cwd = os.getcwd()
print("Current Working Directory:", cwd)
data_dir = f"{cwd}/pysaebm/test/my_data"
data_files = os.listdir(data_dir) 

OUTPUT_DIR = 'algo_results'

with open(f"{cwd}/pysaebm/test/true_order_and_stages.json", "r") as f:
    true_order_and_stages = json.load(f)

for data_file in data_files:
    fname = data_file.replace('.csv', '')
    metadata = true_order_and_stages[fname]
    n_subtypes = metadata['N_SUB']
    true_order_matrix = metadata['TRUE_ORDERINGS']
    true_subtype_assignments = metadata['TRUE_SUBTYPE_ASSIGNMENTS']
    results = run_subebm(
        data_file= os.path.join(data_dir, data_file),
        n_subtypes=n_subtypes,
        true_order_matrix=true_order_matrix,
        true_subtype_assignments=true_subtype_assignments,
        n_subtype_shuffle=2,
        output_dir=OUTPUT_DIR,
        n_iter=2000,
        n_shuffle=2,
        burn_in=100,
        thinning=1,
        seed = 53,
        save_results=True
    )