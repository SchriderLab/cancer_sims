import pandas as pd
import numpy as np
import argparse
import configparser
from itertools import product
from pathlib import Path

parser = argparse.ArgumentParser(
    description='Run monte carlo cancer two-strike therapy SLiM simulations.')


parser.add_argument('config_path', type=str, 
                    help='Path to the configuration file')
parser.add_argument('--load_params', type=str, 
                    help='Path to the parameters file to load (optional)')
parser.add_argument('--params_split', type=int, default=1, help="Number of splits to make in the parameter space")

args = parser.parse_args()

config = configparser.ConfigParser()
config.read(args.config_path)

def construct_params_df():

    section_dfs = []

    for section in config.sections():
        # Parse the range
        start = float(config[section]["Start"])
        end = float(config[section]["End"])
        step = float(config[section]["Step"])
        if start == end:
            values = [start]
        else:
            values = np.arange(start, end + step, step)

        # Parse the parameter names
        param_names = config[section]["Names"].split(", ")

        # Create a DataFrame for this section
        section_df = pd.DataFrame({param: values for param in param_names})
        print(section_df)
        section_dfs.append(section_df)

    # Compute the Cartesian product of all sections
    combined_product = list(product(*[df.values for df in section_dfs]))

    # Flatten the result into a DataFrame
    combined_flat = [tuple(value for row in rows for value in row) for rows in combined_product]

    # Generate column names
    columns = [col for df in section_dfs for col in df.columns]

    # Create the final DataFrame
    combined_df = pd.DataFrame(combined_flat, columns=columns)

    return combined_df

if args.load_params:
    params_df = pd.read_csv(args.load_params)
    print("Using supplied parameter file. Parameters from config file will be ignored.")
else:
    params_df = construct_params_df()


path = config['DEFAULT']['Directory']
script = config['DEFAULT']['Script']
submission_script = config['DEFAULT']['SubmissionScript']
slim_path = config['DEFAULT']['SlimPath']


params_df['param_id'] = range(len(params_df))


params_df_path = Path(path) / 'params.csv'
params_df.to_csv(params_df_path, index=False)

job_scripts = []
for i, params in enumerate(params_df.itertuples(index=False)):
    job_script = slim_path
    for param_name, param_value in zip(params_df.columns, params):
        job_script += f' -d {param_name}={param_value}'
    job_script += f' -d "store_dir=\'{path}\'" -d job_id=$SLURM_ARRAY_TASK_ID {script}'
    job_scripts.append(job_script)

# load the submission script
submission_script = Path(submission_script)
with open(submission_script, 'r') as sub_f:
    submission_script_content = sub_f.read()

for i in range(args.params_split):
    start = i * len(job_scripts) // args.params_split
    end = (i + 1) * len(job_scripts) // args.params_split
    with open(f'run_sims_params_{i+1}.sh', 'w') as f:
        f.write(f'{submission_script_content}\n')
        for job_script in job_scripts[start:end]:
            f.write(f'{job_script}\n')