import itertools
import json
from collections import Counter

import numpy as np
import pandas as pd




data = json.load(open('input/cochanges_in_commit.json'))
for project in data['projects']:
    project_result = {"project": [project['github_url']]}
    combination_ms_changed = list()
    for commit in project['commit']:
        microservices_cochanged = list(commit['microservice_cochanged'])
        unique = set(microservices_cochanged)
        unique = [str(x) for x in unique]

        if 'nan' in unique:
            print(project['github_url'])
            print(unique)
            unique.remove('nan')
        if len(unique) > 1:
            unique.sort()
            combination = list(itertools.combinations(unique, 2))
            combination_ms_changed += combination

    occurences = Counter(combination_ms_changed)

    for occ in occurences.items():
        project_result[occ[0]] = occ[1]

    # for comb in combination_ms_changed:
    #     if comb in project_result:
    #         project_result[comb] += 1
    #     else:
    #         project_result[comb] = 1


    result = pd.DataFrame.from_dict(project_result)
    result.to_csv(f"output/index_row/{project['github_url'].replace('https://github.com/', '').replace('/', '-')}.csv",
                  index=False)
    project_result.pop('project')
    result = pd.DataFrame.from_dict(project_result, orient='index')
    #result = result.iloc[1: , :]
    result.to_csv(f"output/index_column/{project['github_url'].replace('https://github.com/', '').replace('/', '-')}.csv", header=False)





