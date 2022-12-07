import pandas as pd
import pytz
from dateutil import parser

data = pd.read_csv('input/dataset_timestamp_normalized.csv')

projects = data['github_url'].unique()
sr = 'project,first_commit,last_commit\n'
data['committer_timestamp'] = pd.to_datetime(data['committer_timestamp'])
#data['committer_timestamp'] = data.apply(lambda row : parser.parse(row['committer_timestamp']).astimezone(pytz.UTC), axis = 1)
for project in projects:
    loc = data[data['github_url'] == project]
    sr += project + "," + str(loc['committer_timestamp'].min()) + "," + str(loc['committer_timestamp'].max()) + '\n'
with open('output/fist_last_commit.csv', 'w') as file:
    file.write(sr)