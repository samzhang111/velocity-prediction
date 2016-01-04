import pandas as pd
import datetime

stories['created_at'] = pd.to_datetime(stories['created_at'])
stories['accepted_at'] = pd.to_datetime(stories['accepted_at'])
stories['updated_at'] = pd.to_datetime(stories['updated_at'])

stories.sort('created_at', inplace=True)
stories['estimate'].fillna(0, inplace=True)
stories_without_nans = stories.dropna(subset=['accepted_at'])

# Calculate week buckets
def get_week_num_from_date(date):
    first_date = stories['created_at'].head(1).values[0]
    days_since_start = date - first_date
    week_since_start = days_since_start / datetime.timedelta(days=7)
    return math.floor(week_since_start)

import math
stories_without_nans['accepted_at_week'] = stories_without_nans['accepted_at'].apply(get_week_num_from_date)
stories_without_nans['created_at_week'] = stories_without_nans['created_at'].apply(get_week_num_from_date)

story_type_counts_by_created_week = stories_without_nans.groupby(['created_at_week','story_type']).count()['id']

flattened_story_type_counts = story_type_counts_by_created_week.unstack().fillna(0)

velocity_by_week = stories_without_nans.groupby(['accepted_at_week']).sum()['estimate']
flattened_story_type_counts['points'] = velocity_by_week
flattened_story_type_counts.fillna(0, inplace=True)
