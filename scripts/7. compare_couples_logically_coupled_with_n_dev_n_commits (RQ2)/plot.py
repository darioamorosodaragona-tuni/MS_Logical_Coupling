import os

import matplotlib.pyplot as plt
import pandas
from matplotlib.ticker import MaxNLocator
from tqdm import tqdm

files = os.listdir("input/introducing")
plt.rcParams['font.size'] = 14.5
for file in tqdm(files):
    fig, ax = plt.subplots(1)
    introducing = pandas.read_csv(f"input/introducing/{file}")
    n_commits = pandas.read_csv(f"input/n_commits/{file}")
    n_developers = pandas.read_csv(f"input/n_developers/{file}")
    plt.plot(introducing["months"], introducing['ms_lc_introduced'], "-", label="#couples_lc_introduced")
    #plt.plot(introducing["months"], introducing['ms_lc_introduced'], "*")
    plt.plot(n_commits["months"], n_commits['n_commits'], "-", label="#commits")
    #plt.plot(n_commits["months"], n_commits['n_commits'], "*")
    plt.plot(n_developers["months"], n_developers['n_developers'], "-", label="#developers")
    #plt.plot(n_developers["months"], n_developers['n_developers'], "*")
    ticks = [1] + [*range(5, introducing["months"].max() + 1, 5)]
    plt.legend()
    #plt.legend(["#couples_lc_introduced", "", "#commits", "", "#developers"])
    plt.xticks(ticks)
    plt.xlim(1, introducing["months"].max() + 1)
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.savefig(f"output/plot/{file.replace('introducing', 'all').replace('.csv', '.pdf')}")
    plt.close()
