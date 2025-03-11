import numpy as np
import pandas as pd

def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    medal_tally = medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending = False).reset_index()

    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    return medal_tally

def country_year_list(df):
    year = df['Year'].unique().tolist()
    year.sort()
    year.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()

    country.insert(0, 'Overall')

    return year,country

def fetch_medal_tally(df,year,country):
  medal_df = df.drop_duplicates(subset = ['Team','NOC','Games','Year','City','Sport','Event','Medal'])
  flag = 0
  if year == 'Overall' and country == 'Overall':
    temp_df = medal_df
  if year  == 'Overall' and country !='Overall':
    flag = 1
    temp_df = medal_df[medal_df['region']==country]
  if year  != 'Overall' and country =='Overall':
    temp_df = medal_df[medal_df['Year']==int(year)]
  if year  != 'Overall' and country !='Overall':
    temp_df = medal_df[(medal_df['region']==country) & (medal_df['Year']==int(year))]

  if flag == 1:
    x = temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending = False).reset_index()
  else:
    x = temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending = False).reset_index()


  x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

  return x

def participating_nation_over_time(df):
    nation_over_time = df.drop_duplicates(['Year', 'region'])['Year'].value_counts().reset_index().sort_values('Year')
    nation_over_time = nation_over_time.rename(columns={'Year': 'Edition', 'count': 'Number of country'})
    return nation_over_time

def most_successful(df,sport):
  temp_df = df.dropna(subset = ['Medal'])
  if sport != 'Overall':
    temp_df = temp_df[temp_df['Sport']==sport]

  x =  temp_df['Name'].value_counts().reset_index().head(15).merge(df,on = 'Name',how = 'left')[['Name','count','Sport','region']].drop_duplicates('Name')
  x.rename(columns = {'count':'Medals'},inplace = True)
  return x

def medal_year(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == "USA"]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_heat(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df1 = temp_df[temp_df['region'] == country]
    return new_df1


def most_successful_country(df, country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, on='Name', how='left')[
        ['Name', 'count', 'Sport']].drop_duplicates('Name')
    x.rename(columns={'count': 'Medals'}, inplace=True)
    return x