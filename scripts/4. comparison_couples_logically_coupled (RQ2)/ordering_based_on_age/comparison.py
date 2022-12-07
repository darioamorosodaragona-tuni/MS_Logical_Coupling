from enum import Enum

import pandas
import seaborn as sns
from matplotlib import pyplot as plt

palette = sns.color_palette("Set3", 2)

plt.rcParams["figure.figsize"] = [30, 15]


class Period(Enum):
    LAST_COMMIT = "last_commit"


class AGE(Enum):
    DAYS = "age_days"
    MONTHS = "age_months"


def plot(couples_dataset, age_dataset, period, age_measure):
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
    data = r_dataframe.join(age_dataset.set_index('project'), on='project')
    data = data.sort_values(by="project").reset_index()
    data.pop('index')
    data = data.sort_values(by=age_measure)
    ax = data.plot.bar(y='lc_coupled', color=palette[0])
    data["sorted_index"] = range(0, len(data.index))
    ax1 = ax.twinx()
    data.plot.scatter(y=age_measure, x='sorted_index', ax=ax1, secondary_y=True, linewidth=5)
    # ax.set_xticks(first_month.index)
    ax.set_xlabel('Project')
    ax.set_ylabel('# of microservices logically coupled')
    ax1.set_ylabel(f'# age in {age_measure}')
    ax.legend(period)
    plt.savefig(f"output/{period}_{age_measure}_couples_logically_coupled_ordered_by_age.png")
    plt.show()
    plt.close()


if "__main__" == __name__:
    age = pandas.read_csv('input/age.csv')
    age['project'] = [str(x).replace("https://github.com/", "").replace('/', '-') for x in
                      age['project']]

    final = pandas.read_csv('input/final_couples_logically_coupled.csv')
    plot(final, age, period=Period.LAST_COMMIT.value, age_measure=AGE.MONTHS.value)
