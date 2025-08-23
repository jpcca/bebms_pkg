pip install -e .

rm -rf algo_results pympebm/test/algo_results
python3 pympebm/test/test.py
[ -d algo_results ] && mv algo_results pympebm/test/