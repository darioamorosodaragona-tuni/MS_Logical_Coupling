import os

import pandas.errors
from matplotlib import pyplot as plt
import pandas as pd
#bins = list([0,5,10,20,30,40,50,100,200,300])
bins = list(range(0,2001,1))
files = os.listdir('input/index_column')
fig1 = plt.figure()
i = 0
result = {'projects' :[]}
i_project = 0
for file in files:
    try:
        data = pd.read_csv(os.path.join('input/index_column', file), header=None)
    except pandas.errors.EmptyDataError:
         print(file)
         continue

    per_project = {}


    grouped = data.groupby(pd.cut(data.iloc[:,1], bins))[1]
    count = grouped.count()
    count.rename_axis(i, inplace=True)

    result['projects'].append(file.replace(".csv", ''))
    for index, row in count.items():
        i += 1
        if index.right in result:
            result[index.right].append(row)
        else:
            result[index.right] = [row]

    # n = len(result['projects'])
    # for k in result.keys():
    #     if len(result[k]) < n:
    #         result[k] += (n - len(result[k])) * [0]
    i_project += 1

result = pd.DataFrame(result)
#result = result.iloc[: , 1:]
result.to_csv('output/first_commit_couples_logically_coupled.csv', index=False)