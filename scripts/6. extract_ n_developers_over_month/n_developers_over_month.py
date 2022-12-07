import itertools
from collections import Counter

import pandas
import pandas as pd
import pytz
from dateutil import parser
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator
from tqdm import tqdm


def introducing(projects_to_compare, first_last_commits, plot_ax=None):
    for project in tqdm(projects_to_compare):
        index = projects_to_compare.index(project)
        if plot_ax == None:
            fig, ax = plt.subplots(1)
        else:
            ax = plot_ax
        data_to_analyze = data[data["github_url"] == project].copy()
        date_range_data = first_last_commits[
            first_last_commits["project"] == project]
        first_commit = date_range_data['first_commit'].iloc[0]

        data_to_analyze['committer_timestamp'] = data_to_analyze.apply(
            lambda row: parser.parse(row['committer_timestamp']).astimezone(pytz.UTC), axis=1)

        data_to_analyze['group_index'] = data_to_analyze.groupby(pd.Grouper(key='committer_timestamp', axis=0,
                                                                            freq='30d', sort=True,
                                                                            origin=first_commit)).ngroup()
        group_date_range = data_to_analyze.groupby(pd.Grouper(key='committer_timestamp', axis=0,
                                                              freq='30d', sort=True, origin=first_commit))
        n_group = data_to_analyze['group_index'].max() + 1
        result = {"months": list(range(0, n_group)),
                  "n_developers": [0] * n_group}

        couples = []
        last_index = 0
        for group_name, df_group in group_date_range:
            if df_group.empty:
                last_index = last_index + 1
                result['n_developers'][last_index] = 0
            else:
                result['n_developers'][df_group['group_index'].iloc[0]] = len(
                    df_group['author_email'].unique().tolist())
                last_index = df_group['group_index'].iloc[0]

        r = pandas.DataFrame(result)
        r['months'] = r['months'] + 1
        # r['cum'] = r["ms_lc_introduced"].cumsum()
        # r.plot(x="months", y="cum")
        r.set_index(r['months'], inplace=True)
        r.plot(y="n_developers", ax=ax, style="-")
        r.plot(y="n_developers", ax=ax, style="*")
        ticks = [1] + [*range(5, r["months"].max() + 1, 5)]
        plt.xticks(ticks)
        plt.xlim(1, r["months"].max() + 1)
        plt.xlabel("months")
        plt.ylabel("developers")
        plt.legend([])
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        if plot_ax is None:
            plt.savefig(
                f"output/plot/{index}_{project.replace('https://github.com/', '').replace('/', '-')}__introducing")
            plt.close()
        r.to_csv(f"output/csv/{index}_{project.replace('https://github.com/', '').replace('/', '-')}_result.csv")


if __name__ == "__main__":
    data = pd.read_csv("input/dataset.csv")
    data = data[(data['github_url'] != "https://github.com/eko/monday") & (
            data['github_url'] != "https://github.com/hyperscale/hyperpic") & (
                        data['github_url'] != "https://github.com/loft-sh/devspace")]
    projects = data['github_url'].sort_values().unique().tolist()
    with open("output/missing_projects.csv", "w") as file:
        file.write("")
    date_range_data = pd.read_csv("input/fist_last_commit.csv")
    date_range_data['first_commit'] = date_range_data.apply(
        lambda row: parser.parse(row['first_commit']).astimezone(pytz.UTC), axis=1)
    date_range_data['last_commit'] = date_range_data.apply(
        lambda row: parser.parse(row['last_commit']).astimezone(pytz.UTC), axis=1)
    introducing(projects, first_last_commits=date_range_data)
