import numpy as np

def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Medal', 'Event'])
    medal_tally = medal_tally.groupby(['NOC', 'region']).sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    return medal_tally

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, "Overall")

    country = np.unique(df['region'].dropna().values).tolist()
    country.insert(0, 'Overall')

    return years, country

def fetch_medal_tally(df, year, country):
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = df
    elif year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = df[df['region'] == country]
    elif year != 'Overall' and country == 'Overall':
        temp_df = df[df['Year'] == int(year)]
    else:
        temp_df = df[(df['region'] == country) & (df['Year'] == int(year))]

    if flag == 1:
        x = temp_df.groupby(['Year']).sum(numeric_only=True)[['Gold', 'Silver', 'Bronze']].sort_values('Year', ascending=True).reset_index()
    else:
        x = temp_df.groupby(['region']).sum(numeric_only=True)[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']
    return x
