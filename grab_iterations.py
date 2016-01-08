from __future__ import print_function
import requests
import os
import sys
import pandas as pd

API_KEY = os.getenv('TRACKER_API_KEY')
PROJECT_ID = sys.argv[1]
API = "https://www.pivotaltracker.com/services/v5/projects/{project_id}/iterations".format(project_id=PROJECT_ID)

def get_chunk(offset):
    r = requests.get(API,
            headers={'X-TrackerToken' : API_KEY},
            params=dict(
                limit = 100,
                offset = offset,
                fields = 'number,length,team_strength,velocity,analytics,points,effective_points,accepted,story_ids'
                ))
    return r.json()

def fetch_all():
    results = []
    i = 0

    while True:
        print('Grabbing chunk %d' % i)
        chunk = get_chunk(i)
        if i == 0:
            print(chunk)

        if len(chunk) == 0:
            break
        results.extend(chunk)

        i+=len(chunk)

    df = pd.DataFrame(results)
    df.to_csv('tracker-{}-iterations.csv'.format(PROJECT_ID), index=False, encoding='utf-8')

if __name__ == '__main__':
    fetch_all()
