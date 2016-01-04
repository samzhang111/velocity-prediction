import requests
import os
import sys
import pandas as pd

API_KEY = os.getenv('TRACKER_API_KEY')
PROJECT_ID = sys.argv[1]
STORIES_API = "https://www.pivotaltracker.com/services/v5/projects/{project_id}/stories".format(project_id=PROJECT_ID)

def get_chunk(offset):
    r = requests.get(STORIES_API,
            headers={'X-TrackerToken' : API_KEY},
            params=dict(
                limit = 100,
                offset = offset
                ))
    return r.json()

def fetch_all():
    results = []
    i = 0

    while True:
        print 'Grabbing chunk %d' % i
        chunk = get_chunk(i)
        if len(chunk) == 0:
            break
        results.extend(chunk)

        i+=100

    df = pd.DataFrame(results)
    df.to_csv('output.csv', index=False, encoding='utf-8')

if __name__ == '__main__':
    fetch_all()
