import itertools
from collections import Counter

import pandas
import pandas as pd
import pytz
from dateutil import parser
from matplotlib import pyplot, pyplot as plt
from matplotlib.ticker import MaxNLocator
from tqdm import tqdm


# https://github.com/MesutAtasoy/Joker
# https://github.com/cleisommais/journey_full_microservices

def introducing(projects_to_compare, plot_ax=None):
    for project in tqdm(projects_to_compare):
        index = projects_to_compare.index(project)
        if plot_ax == None:
            fig, ax = plt.subplots(1)
        else:
            ax = plot_ax
        data_to_analyze = data[data["github_url"] == project].copy()
        try:
            ms_lc_data = pd.read_csv(
                f"input/index_column/{project.replace('https://github.com/', '').replace('/', '-')}.csv",
                names=["Couple", "#Commit"])
        except:
            with open("output/missing_projects.csv", "a+") as file:
                file.write(project)
                file.write("\n")
            continue
        date_range_data = pd.read_csv("input/fist_last_commit.csv")
        date_range_data = date_range_data[
            date_range_data["project"] == project]
        ms_lc = []

        data_to_analyze['committer_timestamp'] = data_to_analyze.apply(
            lambda row: parser.parse(row['committer_timestamp']).astimezone(pytz.UTC), axis=1)

        ms_lc_data["Couple"].apply(
            lambda x: ms_lc.extend(str(x).replace("(", "").replace(")", "").replace("'", "").split(",")))
        date_range_data['first_commit'] = date_range_data.apply(
            lambda row: parser.parse(row['first_commit']).astimezone(pytz.UTC), axis=1)
        date_range_data['last_commit'] = date_range_data.apply(
            lambda row: parser.parse(row['last_commit']).astimezone(pytz.UTC), axis=1)
        first_commit = date_range_data['first_commit'].iloc[0]

        data_to_analyze['group_index'] = data_to_analyze.groupby(pd.Grouper(key='committer_timestamp', axis=0,
                                                                            freq='30d', sort=True,
                                                                            origin=first_commit)).ngroup()
        group_date_range = data_to_analyze.groupby(pd.Grouper(key='committer_timestamp', axis=0,
                                                              freq='30d', sort=True, origin=first_commit))
        n_group = data_to_analyze['group_index'].max() + 1
        result = {"months": list(range(0, n_group)),
                  "ms_lc_introduced": [0] * n_group}

        couples = []
        for group_name, df_group in group_date_range:
            commits = df_group['commit_hash'].unique()
            for commit in commits:
                couples_hold = couples.copy()
                _loc = df_group[df_group['commit_hash'] == commit]
                microservices_changed = _loc['service_name'].unique().tolist()
                microservices_changed = [str(x) for x in microservices_changed]

                if 'nan' in microservices_changed:
                    microservices_changed.remove('nan')
                if len(microservices_changed) > 1:
                    microservices_changed.sort()
                    combination = list(itertools.combinations(microservices_changed, 2))
                    couples += combination
                occurences = Counter(couples)
                prev_ocrrences = Counter(couples_hold)
                for occ in occurences.items():
                    if occ[1] >= 5 and prev_ocrrences[occ[0]] < 5:
                        result['ms_lc_introduced'][_loc['group_index'].iloc[0]] += 1
        r = pandas.DataFrame(result)
        r['months'] = r['months'] + 1
        # r['cum'] = r["ms_lc_introduced"].cumsum()
        # r.plot(x="months", y="cum")
        r.set_index(r['months'], inplace=True)
        r.plot(y="ms_lc_introduced", ax=ax, style="-")
        r.plot(y="ms_lc_introduced", ax=ax, style="*")
        ticks = [1]+[*range(5, r["months"].max() + 1, 5)]
        plt.xticks(ticks)
        plt.xlim(1, r["months"].max() + 1)
        plt.xlabel("months")
        plt.ylabel("couples logical coupled")
        plt.legend([])
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        if plot_ax is None:
            pyplot.savefig(f"output/plot/{index}_{project.replace('https://github.com/', '').replace('/', '-')}__introducing")
            pyplot.close()
        r.to_csv(f"output/csv/{index}_{project.replace('https://github.com/', '').replace('/', '-')}_result.csv")


if __name__ == "__main__":
    fig, ax = plt.subplots(1)
    data = pd.read_csv("input/dataset.csv")
    data = data[(data['github_url'] != "https://github.com/eko/monday")  & (data['github_url'] != "https://github.com/hyperscale/hyperpic") & (data['github_url'] != "https://github.com/loft-sh/devspace")]
    projects = data['github_url'].sort_values().unique().tolist()
    i = 0
    with open("output/index.csv", "w") as file:
        for p in projects:
            file.write(f"{str(i)},{p.replace('https://github.com/', '').replace('/', '-')}\n")
            i += 1

    with open("output/missing_projects.csv", "w") as file:
         file.write("")
    introducing(projects)
    #introducing(["https://github.com/DenisBiondic/RealTimeMicroservices", "https://github.com/MesutAtasoy/Joker"], ax)
    # ax.legend([4,36])
    # pyplot.savefig("output/compare_introducing")
