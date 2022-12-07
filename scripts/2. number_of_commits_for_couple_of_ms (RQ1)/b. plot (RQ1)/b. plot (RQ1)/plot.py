import pandas
from matplotlib import pyplot as plt
import seaborn as sns
from matplotlib.ticker import MaxNLocator

result = pandas.read_csv('input/plot.csv')
palette = sns.color_palette("Set3", 3)
plt.rcParams['font.size'] = 8.5
#plt.rcParams["figure.figsize"] = [30, 15]
# r = {'project' : [],
#     'lc_coupled': [],
#     'not_coupled': []}
r = {'project': [],
     'lc_coupled': []}
i_project = 0
for index, row in result.iterrows():
    coupled = row.iloc[5:]
    sum = coupled.sum()
    r['project'].append(i_project)
    i_project += 1
    r["lc_coupled"].append(sum)
    # not_coupled = row.iloc[0:4].sum()
    # r["not_coupled"].append(not_coupled)

r_dataframe = pandas.DataFrame(r)
r_dataframe.to_csv("output/number_of_couples_logically_coupled_per_project.csv", index=False)

bins = [*range(1, 820, 5)]
binned = pandas.DataFrame()
binned['bin'] = pandas.cut(r_dataframe["lc_coupled"], bins)
df2 = binned.groupby('bin').bin.count()
fif, ax = plt.subplots(1)
#ax.set_xscale("log")
r_dataframe.lc_coupled.plot(kind='hist', ax=ax, bins=bins, color = palette[2])

# to_plot = {"#couples_lc_coupled": [],
#            "#project": []}
# for index, value in binned.iteritems():
#     to_plot["#couples_lc_coupled"].append(index.right)
#     to_plot["#project"].append(value)
#
# to_plot_d = pandas.DataFrame(to_plot)
# to_plot_d = to_plot_d.sort_values(by="#couples_lc_coupled")
#to_plot_d = to_plot_d[to_plot_d["#project"] > 0]

#r_dataframe.hist(ax=ax, bins=15)
#to_plot_d.plot.bar(x="#couples_lc_coupled", y="#project", ax=ax, color = palette[2])
# to_plot_d.plot(x="#couples_lc_coupled", y="#project", ax = ax, style="r-")

# plt.bar(to_plot_d["#couples_lc_coupled"], to_plot_d["#project"])
# plt.xlim(0,1000)
# plt.xticks(bins)
plt.legend("")
plt.xlabel("# couples lc coupled")
plt.ylabel("# projects")
ax.yaxis.set_major_locator(MaxNLocator(integer=True))
plt.xlim(1, bins[-1])
ticks = [*range(0,820,50)]
ticks.pop(0)
ticks[0] = 1
ticks.insert(1, 50)
plt.xticks(ticks)
ax.set_yscale("log")
# plt.plot(to_plot_d["#couples_lc_coupled"], to_plot_d["#project"], '-')


# ax = r_dataframe['lc_coupled'].plot.bar()
# #ax = r_dataframe[['lc_coupled', "not_coupled"] ].plot.bar(stacked=True)
#
# #ax = result.T.b. plot (RQ1) (RQ1).bar(stacked=False)
# plt.xlabel('Project')
# plt.ylabel('# couples of microservices')
# for c in ax.containers:
#     # Optional: if the segment is small or 0, customize the labels
#     labels = [v.get_height() if v.get_height() > 0 else '' for v in c]
#
#     # remove the labels parameter if it's not needed for customized labels
#     ax.bar_label(c, labels=labels, label_type='center')
# #
# #
# #
# #
# plt.legend(bbox_to_anchor=(1.04, 0.5), loc="center left", borderaxespad=0)

plt.savefig('output/couples_of_ms_1.png', bbox_inches = "tight")
plt.show( bbox_inches = "tight")
plt.close()


bins = [*range(0, 80, 5)] + [1000]
bins.pop(0)
bins.insert(0,1)
binned = pandas.DataFrame()
binned['bin'] = pandas.cut(r_dataframe["lc_coupled"], bins)
df2 = binned.groupby('bin').bin.count()
fif, ax = plt.subplots(1)
#ax.set_xscale("log")
r_dataframe.lc_coupled.plot(kind='hist', ax=ax, bins=bins, color = palette[2])
plt.legend("")
plt.xlabel("# couples lc coupled")
plt.ylabel("# projects")
ax.yaxis.set_major_locator(MaxNLocator(integer=True))
plt.xlim(1, bins[-1])
# ticks = [*range(0,820,50)]
# ticks.pop(0)
# ticks[0] = 1
# ticks.insert(1, 50)
# plt.xticks(ticks)
ax.set_yscale("log")
plt.savefig('output/couples_of_ms_2.png', bbox_inches = "tight")
plt.show( bbox_inches = "tight")
plt.close()

