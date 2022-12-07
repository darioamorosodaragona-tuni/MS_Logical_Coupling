from enum import Enum

import pandas
import seaborn as sns
from matplotlib import pyplot as plt

palette = sns.color_palette("Set3", 2)
plt.rcParams["figure.figsize"] = [30, 15]


class Period(Enum):
    LAST_COMMIT = "last_commit"
    FIRST_COMMIT = "first_commit"


def plot(n_developers, couples_dataset, period):
    r = {'project': [],
         'lc_coupled': []}
    i_project = 0
    for index, row in couples_dataset.iterrows():
        coupled = row.iloc[5:]
        sum = coupled.sum()
        r['project'].append(row['projects'])
        i_project += 1
        r["lc_coupled"].append(sum)
        # not_coupled = row.iloc[0:4].sum()
        # r["not_coupled"].append(not_coupled)

    r_dataframe = pandas.DataFrame(r)
    data = r_dataframe.join(n_developers.set_index('project'), on='project')
    data = data.sort_values(by="project").reset_index()
    data.pop('index')
    data = data.sort_values(by='n_developers')
    ax = data.plot.bar(y='lc_coupled', color=palette[0])
    data["sorted_index"] = range(0, len(data.index))
    ax1 = ax.twinx()
    data.plot.scatter(y='n_developers', x='sorted_index', ax=ax1, secondary_y=True, linewidth=5)
    ax.set_xlabel('Project')
    ax.set_ylabel('# couples of microservices logically coupled')
    ax1.set_ylabel('# of developers')
    plt.savefig(f"output/{period}_couples_logically_coupled_ordered_by_n_developers.png")
    plt.show()
    plt.close()


if "__main__" == __name__:
    n_developers = pandas.read_csv('input/n_developers_first_commit.csv')
    n_developers['project'] = [str(x).replace("https://github.com/", "").replace('/', '-') for x in
                               n_developers['project']]

    couples_dataset = pandas.read_csv('input/first_commit_couples_logically_coupled.csv')
    plot(n_developers, couples_dataset, Period.FIRST_COMMIT.value)

    #LAST COMMIT

    n_developers = pandas.read_csv('input/final_n_developers.csv')
    n_developers['project'] = [str(x).replace("https://github.com/", "").replace('/', '-') for x in
                               n_developers['project']]

    couples_dataset = pandas.read_csv('input/final_couples_logically_coupled.csv')
    plot(n_developers, couples_dataset, Period.LAST_COMMIT.value)



