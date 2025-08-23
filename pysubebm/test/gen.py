from pysubebm import generate, get_params_path
import numpy as np 
import json 
import re 
import os 

def extract_components(filename):
    pattern = r'^j(\d+)_r([\d.]+)_E(.*?)_m(\d+)$'
    match = re.match(pattern, filename)
    if match:
        return match.groups()  # returns tuple (J, R, E, M)
    return None

experiment_names = [
    "sn_kjOrdinalDM_xnjNormal",     # Experiment 1: Ordinal kj with Dirichlet-Multinomial, Normal Xnj
    "sn_kjOrdinalDM_xnjNonNormal",  # Experiment 2: Ordinal kj with Dirichlet-Multinomial, Non-Normal Xnj
    # "sn_kjOrdinalUniform_xnjNormal", # Experiment 3: Ordinal kj with Uniform distribution, Normal Xnj
    # "sn_kjOrdinalUniform_xnjNonNormal", # Experiment 4: Ordinal kj with Uniform distribution, Non-Normal Xnj
    # "sn_kjContinuousUniform",       # Experiment 5: Continuous kj with Uniform distribution
    # "sn_kjContinuousBeta",          # Experiment 6: Continuous kj with Beta distribution
    # "xiNearNormal_kjContinuousUniform", # Experiment 7: Near-normal Xi with Continuous Uniform kj
    # "xiNearNormal_kjContinuousBeta", # Experiment 8: Near-normal Xi with Continuous Beta kj
    # "xiNearNormalWithNoise_kjContinuousBeta", # Experiment 9: Same as Exp 8 but with noises to xi
]

def convert_np_types(obj):
    """Convert numpy types in a nested dictionary to Python standard types."""
    if isinstance(obj, dict):
        return {k: convert_np_types(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_np_types(item) for item in obj]
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return convert_np_types(obj.tolist())
    else:
        return obj


if __name__ == '__main__':
    rng = np.random.default_rng(53)

    OUTPUT_DIR = 'my_data'
    # Get path to default parameters
    params_file = get_params_path()

    with open(params_file) as f:
        params = json.load(f)

    JS = [100, 500, 1000]
    RS = [0.1, 0.5, 0.9]
    MS = range(1, 20)

    all_exp_dicts = []
    for exp_name in experiment_names:
        random_state = rng.integers(0, 2**32 - 1)
        exp_dict = generate(
            experiment_name = exp_name,
            params_file=params_file,
            js = [200],
            rs = [0.1],
            num_of_datasets_per_combination=3,
            output_dir=OUTPUT_DIR,
            seed=random_state,
            keep_all_cols = False,
            fixed_biomarker_order = True, # important
            save2file=False,
        )
        all_exp_dicts.append(exp_dict)

    # flatten the dictionaries
    combined = {k: v for d in all_exp_dicts for k, v in d.items()}
    # convert numpy types to python standards types in order to save to json
    combined = convert_np_types(combined)

    # Dump the JSON
    with open(f"true_order_and_stages.json", "w") as f:
        json.dump(combined, f, indent=2)

    