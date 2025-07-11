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


def data_over_time(df, col):
    temp_df = df.drop_duplicates(['Year', col])
    result = temp_df.groupby('Year').count()[col].reset_index()
    result.rename(columns={'Year': 'Edition', col: f'{col} Count'}, inplace=True)
    return result

def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    top_athletes = temp_df['Name'].value_counts().reset_index().head(15)
    top_athletes.columns = ['Name', 'Medal Count']

    merged = top_athletes.merge(df, on='Name', how='left')[['Name', 'Medal Count', 'region', 'Sport']].drop_duplicates('Name')

    return merged

def country_medal_tally(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Medal', 'Event'], inplace=True)

    if country == 'Overall':
        medal_tally = temp_df.groupby('Year').size().reset_index(name='Medal Count')
    else:
        country_df = temp_df[temp_df['region'] == country]
        medal_tally = country_df.groupby('Year').size().reset_index(name='Medal Count')

    return medal_tally

