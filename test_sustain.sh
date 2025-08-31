pip install -e .

# TQDM_DISABLE=1 

rm -rf sustain_results pysubebm/test/sustain_results
python3 pysubebm/test/test_sustain.py
[ -d sustain_results ] && mv sustain_results pysubebm/test/