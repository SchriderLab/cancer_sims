from pathlib import Path
import pandas as pd
from tqdm import tqdm
import argparse
import numpy as np

def parse_data(sim_dir, output_file):
    params_file = sim_dir / "params.csv"
    params_df = pd.read_csv(params_file)
    fraction_extinct = []
    mut_rates = []
    second_strike_lags = []
    for params_df_row in tqdm(params_df.iterrows(), total=len(params_df)):
        mut_rate = params_df_row.mut_rate
        second_strike_lag = params_df_row.second_strike_lag
        param_id = params_df_row.param_id
        #fitness_cost = params_df_row.fitness_cost
        rep_final_Ns = []
        replicate_files = list(sim_dir.glob(f"log_{param_id}_*.csv"))
        for rep_file in replicate_files:
            file_df = pd.read_csv(rep_file)
            file_df.fillna(0, inplace=True)
            final_N = file_df.iloc[-1].N
            rep_final_Ns.append(final_N)
        fraction_extinct.append(np.mean([N == 0 for N in rep_final_Ns]))
        mut_rates.append(mut_rate)
        second_strike_lags.append(second_strike_lag)

    results_df = pd.DataFrame({
        "mut_rate": mut_rates,
        "second_strike_lag": second_strike_lags,
        "fraction_extinct": fraction_extinct
    })
    results_df = results_df.sort_values(by=["mut_rate", "second_strike_lag"])
    results_df.to_csv(output_file, index=False)

if __name__ == "__main__":
    argpaser = argparse.ArgumentParser()
    argpaser.add_argument("--sims_dir", type=str, help="Path to the directory containing the simulation output files", required=True)
    argpaser.add_argument("--output", type=str, help="Path to the outputfile", required=True)

    args = argpaser.parse_args()
    sims_dir = Path(args.sims_dir)
    output_file = Path(args.output)