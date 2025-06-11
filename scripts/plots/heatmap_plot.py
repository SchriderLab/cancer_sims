import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from argparse import ArgumentParser

argparser = ArgumentParser(description="Plot a heatmap from a CSV file.")
argparser.add_argument("input_file", type=Path, help="Input CSV file containing the data.")
argparser.add_argument("output_file", type=Path, help="Output file to save the heatmap.")

def plot_combo_heatmap(input_file, output_file, mut_rate, x_var, x_label, y_var, y_label, z_var, z_label):
    # Load data
    data = pd.read_csv(input_file)
    #data = data[data[y_var] == mut_rate]
    #data[y_var] = data[y_var] * 1000
    #data['mutation_rate'] = data['mutation_rate'] * 1000
    #data = data[data['mutation_rate'] == mut_rate]
    #data = data[data['combo_dose'] == 0.45]
    #mut_rates = data[y_var].unique().tolist()
    # between each two mutation rates, add another mutation rate that is halfway between the two
    #mut_rates.sort()



    X = data[x_var].unique().tolist()
    X.sort()
    Y = data[y_var].unique().tolist()
    Y.sort(reverse = True)


    Z_arr = np.zeros((len(Y), len(X)))

    for i, y in enumerate(Y):
        for j, x in enumerate(X):
            Z_arr[i, j] = data[(data[y_var] == y) & (data[x_var] == x)][z_var].values[0]


    X_arr, Y_arr = np.meshgrid(X, Y)



    cm = plt.pcolormesh(X_arr, Y_arr, Z_arr, shading='auto', cmap='Spectral_r')

    # for i, row in enumerate(Z_arr[::-1]):
    #     combo_val = row[0]
    #     plt.text(0, Y[::-1][i], f'{combo_val:.2f}', ha='center', va='center')
    #     max_sequential_val = np.max(row[1:])
    #     max_sequential_idx = np.where(row[1:] == max_sequential_val)[0][0]
    #     plt.text(X[max_sequential_idx + 1], Y[::-1][i], f'{max_sequential_val:.2f}', ha='center', va='center')
    max_idx = []
    for row in Z_arr:
        max_val = np.max(row)
        max_idx.append(np.where(row == max_val)[0])
    
    for i, row in enumerate(max_idx):
        max_z_val = Z_arr[i, row]
        print(max_z_val)
        if (max_z_val > 0).all():
            plt.scatter(X_arr[i, row], Y_arr[i, row], color='black', marker='*', s=100)

    # change the ytick at 0 to the word 'Combination'
    # xtick_labels = [f'{int(x)}' for x in X]
    # xtick_labels[0] = 'Combination'
    # xtick_positions = [int(x) for x in np.arange(len(X))]

    # ax = plt.gca()
    # ax.set_xticks(xtick_positions)
    # ax.set_xticklabels(xtick_labels, rotation=90)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    plt.colorbar(label=z_label, mappable=cm)

    plt.tight_layout()
    plt.savefig(output_file, bbox_inches='tight')
    plt.close()

y_var = 'mutation_rate'
y_label = 'Mutation Rate'
#y_var = 'mutation_rate
x_var = 'second_strike_lag'
x_label = 'Second Strike Lag'
z_var = 'extinction_prob'
z_label = 'Extinct Fraction'

data_file = "../cancer_corbin/data/results_drug1lesseff_extinctprob.csv"

df = pd.read_csv(data_file)
plot_combo_heatmap(data_file, './graphs/dfe/drug1lesseff_2.svg', 1.5e-08, x_var, x_label, y_var, y_label, z_var, z_label)
# mut_rates = df['mutation_rate'].unique().tolist()
# for mut_rate in mut_rates:
#     output_file = f'./graphs/combo_vs_seq_withcross/combo_vs_seq_withcross_{mut_rate}.svg'
#     plot_combo_heatmap(data_file, output_file, mut_rate, x_var, x_label, y_var, y_label, z_var, z_label)