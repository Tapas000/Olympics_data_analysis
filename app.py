import streamlit as st
import pandas as pd
import plotly.express as px
import preprocessor , helper
import matplotlib.pyplot as plt
import  seaborn as sns
import plotly.figure_factory as ff
df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

from helper import medal_tally

df = preprocessor.preprocess(df,region_df)
st.sidebar.title("Olympics Analysis")
user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis')
)
#st.dataframe(df)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    year,country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year",year)
    selected_country = st.sidebar.selectbox("Select Country",country)
    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) +" Olympics")

    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country +"overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country +"performance in " + str(selected_year) +"Olympics")

    st.table(medal_tally)

st.title("Top Statistics")
if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athlete = df['Name'].unique().shape[0]
    nation = df['region'].unique().shape[0]

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Cities")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Athlete")
        st.title(athlete)
    with col3:
        st.header("Region")
        st.title(nation)

    nation_over_time =  helper.participating_nation_over_time(df)
    fig = px.line(nation_over_time, x='Edition', y='Number of country')
    st.title("Participating nation over the years")
    st.plotly_chart(fig)

    st.title("Number of Events over time")
    fig,ax = plt.subplots(figsize = (20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)

    st.title("Most Successful Athlete")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport = st.selectbox("select a sport",sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)


if user_menu =='Country-wise Analysis':
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    st.sidebar.title('Country-wise Analysis')
    selected_country =  st.sidebar.selectbox("select a country",country_list)
    final_df = helper.medal_year(df,selected_country)
    fig = px.line(final_df, x='Year', y='Medal')
    st.title(selected_country + " Medals tally over years")
    st.plotly_chart(fig)

    st.title("Country performance in different events over year")
    fig, ax = plt.subplots(figsize=(20, 20))
    x = helper.country_heat(df,selected_country)
    ax = sns.heatmap(
        x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
        annot=True)
    st.pyplot(fig)

    st.title("Most successful athlete of "+ selected_country +' country')

    x = helper.most_successful_country(df, selected_country)
    st.table(x)


# if user_menu == 'Athlete wise Analysis':
#     athlete_df = df.drop_duplicates(subset=['Name', 'region'])
#     x1 = athlete_df['Age'].dropna()
#     x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
#     x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
#     x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
#
#     fig = ff.create_distplot([x1, x2, x3, x4], ['overall age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
#                              show_hist=False, show_rug=False)
#
#     st.plotly_chart(fig)



