# FreshFlow NumPy Capstone - Beginner Version

## Run the project
1. Open this folder in pycharm.
2. Open Terminal in this folder.
3. Run `python make_test_data.py`.
4. Run `python freshflow_analysis.py`.

If NumPy is missing, run `python -m pip install numpy`.

## Files
- `make_test_data.py`: creates a synthetic 500-row CSV with a fixed random seed.
- `freshflow_sales.csv`: generated practice dataset.
- `freshflow_analysis.py`: beginner-friendly analysis for Tasks A-L.
- `anomaly_register.csv`: generated when the analysis script runs.
- `analysis_output.txt`: sample output from a successful run.
- `Final_Report.md`: report draft to review and personalise.
- `requirements.txt`: NumPy dependency.

## Dataset note
The assignment specification says the CSV is not supplied and asks for a generated dataset. This project therefore creates synthetic practice data, not real company transactions. It contains 500 rows, 12 numeric columns and intentional data-quality examples. Some issues may occur in the same row.

## Learning note
The script uses short functions, loops, Boolean masks and basic NumPy operations.
