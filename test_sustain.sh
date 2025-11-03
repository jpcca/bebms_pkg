pip install -e .

# TQDM_DISABLE=1 

rm -rf sustain_results bebms/test/sustain_results
python3 bebms/test/test_sustain.py
[ -d sustain_results ] && mv sustain_results bebms/test/