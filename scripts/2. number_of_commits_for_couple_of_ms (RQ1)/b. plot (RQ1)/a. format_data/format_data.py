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
    result['projects'].append(file.replace(".csv", ""))
    try:
        data = pd.read_csv(os.path.join('input/index_column', file), header=None)
    except pandas.errors.EmptyDataError:

        for index in bins:
            if index == 0:
                continue
            if index in result:
                result[index].append(0)
            else:
                result[index] = [0]
        continue

            #print(file)


    per_project = {}

    grouped = data.groupby(pd.cut(data.iloc[:,1], bins))[1]
    count = grouped.count()
    count.rename_axis(i, inplace=True)

    for index, row in count.items():
        if index.right in result:
            result[index.right].append(row)
        else:
            result[index.right] = [row]


result = pd.DataFrame(result)
result.to_csv('output/final_couples_logically_coupled.csv', index=False)