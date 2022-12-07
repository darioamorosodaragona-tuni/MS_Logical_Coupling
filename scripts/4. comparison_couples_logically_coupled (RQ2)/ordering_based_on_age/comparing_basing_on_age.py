import pandas
from matplotlib import pyplot as plt
import seaborn as sns

palette = sns.color_palette("Set3", 3)

plt.rcParams["figure.figsize"] = [30, 15]

age_dataset = pandas.read_csv('input/age.csv')

age_dataset['project'] = [str(x).replace("https://github.com/", "").replace('/', '-') for x in age_dataset['project']]

first_month = pandas.read_csv('input/first_commit_couples_logically_coupled.csv')
final = pandas.read_csv('input/final_couples_logically_coupled.csv')

r_first = {'project': [],
     'lc_coupled': []}

for index, row in first_month.iterrows():
    coupled = row.iloc[5:]
    sum = coupled.sum()
    r_first['project'].append(row['projects'])
    r_first["lc_coupled"].append(sum)


r_final = {'project': [],
     'lc_coupled': []}

for index, row in final.iterrows():
    coupled = row.iloc[5:]
    sum = coupled.sum()
    r_final['project'].append(row['projects'])
    r_final["lc_coupled"].append(sum)


r_first = pandas.DataFrame(r_first)
r_final = pandas.DataFrame(r_final)


combined = r_first.set_index('project').join(r_final.set_index('project'), on='project', rsuffix='_final', how="right").join(
    age_dataset.set_index('project'), on='project')

combined = combined.sort_values(by="project")
combined.reset_index(inplace=True)
combined = combined.sort_values(by="age_months")
ax = combined[['lc_coupled', 'lc_coupled_final']].plot.bar(color=[palette[0], palette[2]])
combined["sorted_index"] = range(0, len(combined.index))
ax1 = ax.twinx()
combined.plot.scatter(y='age_months', x='sorted_index', ax=ax1, secondary_y=True, linewidth=5)
ax.set_xlabel('Project')
ax.set_ylabel('# couples of microservices logically coupled')
ax.legend(['first month', 'last commit'])
plt.savefig("output/comparison_couples_logically_coupled.png")
plt.show()
