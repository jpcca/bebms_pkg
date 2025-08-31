pip install -e .

rm -rf algo_results pysubebm/test/algo_results
python3 pysubebm/test/test.py
[ -d algo_results ] && mv algo_results pysubebm/test/