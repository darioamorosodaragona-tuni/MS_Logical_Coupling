import pandas
from matplotlib import pyplot as plt
import seaborn as sns
from matplotlib.ticker import ScalarFormatter

palette = sns.color_palette("Set3", 3)
plt.rcParams['font.size'] = 10

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

combined = r_first.set_index('project').join(r_final.set_index('project'), on='project', rsuffix='_final', how="right")
combined = combined.fillna(0)

combined = combined.sort_values(by='project')
ax = combined[combined['lc_coupled_final'] > 0].reset_index().sort_values(by='lc_coupled_final')[
    ['lc_coupled', 'lc_coupled_final']].plot.bar(color=[palette[0], palette[2]], figsize=(11.5, 3))


ax.set_xlabel('project IDs')
ax.set_ylabel('# couples of microservices logically coupled')
ax.legend(['first month', 'last commit'])
ax.set_yscale("log")
ax.yaxis.set_major_formatter(ScalarFormatter())
plt.savefig("output/comparison_couples_logically_coupled.pdf", bbox_inches='tight')
plt.show()

combined['differences'] = combined["lc_coupled_final"] - combined['lc_coupled']
combined = combined.fillna(0)

#plt.rcParams['font.size'] = 10
#combined['differences'] = combined['differences'] + 1
plt.rcParams['font.size'] = 12.5
ax = combined[combined['lc_coupled_final'] > 0].boxplot(column="differences")
# plt.yticks(range(int(combined['differences'].min()), int(combined['differences'].max()),5))

plt.ylabel('# variation coupled ms logically coupled over time')
plt.xlabel("")
#plt.ylim(10**-100, 10**5)
ax.set_yscale("symlog")
ax.yaxis.set_major_formatter(ScalarFormatter())
plt.xticks([])
plt.savefig("output/differences_couples_logically_coupled.pdf",  bbox_inches='tight')
plt.show()
