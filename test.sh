pip install -e .

rm -rf algo_results bebms/test/algo_results
python3 bebms/test/test.py
[ -d algo_results ] && mv algo_results bebms/test/