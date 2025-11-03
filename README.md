# `pysubebm`


## Installation

```bash
pip install bebms=
```

or git clone this project, and then

```bash
pip install -e .
```


## Generate synthetic data

Git clone this repository, and at the root, run

```bash
bash gen.sh
```

The generated data will be found at `[bebms/test/my_data](bebms/test/my_data/)` as `.csv` files. 

The parameters are pre-set and can be found at `[bebms/data/params.json](bebms/data/params.json)`. You can modify the parameters by modifying the `json` file. 

You can also change parameters in `config.toml` to adjust what data to generate.

## Run `bebms` algorithm 

To run `bebms`, after git cloning this repository, at the root, run 

```bash
bash test.sh
```

You can check `[bebms/test/test.py](bebms/test/test.py)` to learn how to use the `[run_bebms](bebms/run.py)` function. 

The results will be saved in the folder of `[bebms/test/algo_results](bebms/test/algo_results/)`.

### Compare with SuStaIn

You can also compare the results of `bebms` with those of SuStaIn.

First, you need to install packages required by SuSta

```bash
pip install git+https://github.com/noxtoby/awkde
pip install git+https://github.com/hongtaoh/ucl_kde_ebm
pip install git+https://github.com/hongtaoh/pySuStaIn
```

Then, at the root of this repository, run 

```bash
bash test_sustain.sh
```

You can check details at `[bebms/test/test_sustain.py](bebms/test/test_sustain.py)`.

The results will be saved in the folder of `[bebms/test/sustain_results](bebms/test/sustain_results/)`.

### Save comparison results

You can save the results of `bebms` along with those of SuStaIn by running at the root:

```bash
python3 save_csv.py
```

The results will be found at the root as `all_results.csv`. 

## Use your own data

You can use your own data. But make sure that your data follows the format as in data in `[bebms/data/samples](bebms/data/samples/)`.


## Changelogs

- 2025-08-21 (V 0.0.3)
    - Did the `generate_data.py`.
- 2025-08-22 (V 0.0.5)
    - Did the `mh.py`
    - Correct conjugate_priors implementation.
- 2025-08-23 (V 0.1.2)
    - Improved functions in `utils.py`.
- 2025-08-29 (V 0.1.3)
    - Didn't change much. 
- 2025-08-30 (V 0.1.8)
    - Optimized `compute_likelihood_and_posteriors` such that we only calculate healthy participants' ln likelihood once every time. 
    - Made sure subtype assignment accuracy does not apply to healthy participants at all. 
    - Fixed a major bug in data generation. The very low subtype assignment might be due to this error.
    - Included both subtype accuracy in `run.py`. 
- 2025-08-31 (V 0.2.5)
    - Resacle event times and disease stages for exp7-9 such that max(event_times) = max_stage -1, and max(disease_stages) = max_stage. 
    - Changed the experiments and some of the implementation. 
    - Forcing `max(event_times) = max_stage -1`, but not forcing disease stages. 
- 2025-09-01 (V 0.2.9)
    - REMOVED THE Forcing `max(event_times) = max_stage -1`
    - Modified the `run.py`.
- 2025-09-02 (V 0.3.3.1)
    - Redid the staging and subtyping. 
    - Integrated with labels and not. 
- 2025-09-04 (V 0.3.3.2)
    - Made sure in staging with labels, the new_order indices starts from 1 instead of 0. This is because participant stages now start from 0.
- 2025-09-06 (V 0.3.5.6)
    - Added the plot function back.
- 2025-09-08 (V 0.3.5.8)
    - Added `ml_subtype` in output results. 
    - Added all_logs to the output returned in `run.py`.
- 2025-09-21 (V 0.3.9)
    - Removed `iteration >= burn_in` when updating best_*. 
- 2025-11-03 (V 0.4.1)
    - Changed the package name to `bebms`. 
    - Edited README. 