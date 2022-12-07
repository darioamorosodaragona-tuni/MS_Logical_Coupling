import json

import matplotlib.pyplot as plt
import pandas as pd
import pytz
from dateutil import parser


def lc_in_single_commit(data):
    result = {
        'projects': list()

    }
    projects = data['github_url'].unique()
    sr = 'project,n_commits,total_ms_changed,total_commits\n'
    for project in projects:

        project_result = {'github_url': project,
                          'commit': list()}

        loc = data[data['github_url'] == project]
        commits = loc['commit_hash'].unique()
        total_ms_changed = 0
        for commit in commits:
            _loc = loc[loc['commit_hash'] == commit]
            microservices_changed = _loc['service_name'].unique()
            microservices_changed = [str(x) for x in microservices_changed]
            if 'nan' in microservices_changed:
                microservices_changed.remove('nan')

            if len(microservices_changed) > 1:
                cochanged = {
                    'microservice_cochanged': microservices_changed,
                    'commit_hash': commit,
                    'developer': _loc['committer_email'].unique()[0],
                    'timestamp' : str(parser.parse(_loc['committer_timestamp'].iloc[0]).astimezone(pytz.UTC))
                }
                total_ms_changed += len(microservices_changed)
                #print(_loc['github_url'].unique())
                project_result['commit'].append(cochanged)

        if len(project_result['commit']) > 0:
            sr += str(project_result['github_url']) + "," + str(len(project_result['commit'])) + "," + str(total_ms_changed) + ',' + str(len(commits)) + '\n'
            result['projects'].append(project_result)


    with open('output/cochanges_in_commit.json', 'w', encoding='utf-8') as file:
        json.dump(result, file)
    with open('output/cochanges_in_commit.csv', 'w', encoding='utf-8') as file:
        file.write(sr)



if __name__ == '__main__':
    data = pd.read_csv('input/dataset.csv')
    lc_in_single_commit(data)
    result = pd.read_csv('output/cochanges_in_commit.csv')
    plt.rcParams["figure.figsize"] = [30, 15]

    plt.bar(range(0, len(result['n_commits'])), result['n_commits'] )
    plt.xlabel('projects')
    plt.ylabel("# commits changing different ms")
    plt.savefig('output/absolute_commits_changing_different_ms.png')
    plt.close()

    plt.bar(range(0, len(result['n_commits'])), result['n_commits']/result['total_commits'] * 100)
    plt.xlabel('projects')
    plt.ylabel("# relative commits changing different ms")
    plt.savefig('output/relative_commits_changing_different_ms.png')
    plt.close()
