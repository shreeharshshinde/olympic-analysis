import streamlit as st
import pandas as pd
import numpy as np
import preprocessor
import helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")

df = pd.read_csv('data/athlete_events.csv')
region_df = pd.read_csv('data/noc_regions.csv')

df = preprocessor.preprocess(df, region_df)

st.sidebar.title("Olympics Analysis")

user_menu = st.sidebar.radio(
    "Select an Option",
    ("Medal Tally", "Overall Analysis", "Country-wise Analysis", "Athlete-wise Analysis")
)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)
    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    if selected_country == 'Overall' and selected_year == 'Overall':
        st.title("Overall Tally")
    elif selected_country == 'Overall' and selected_year != 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    elif selected_country != 'Overall' and selected_year == 'Overall':
        st.title(selected_country + " Overall Performance")
    else:
        st.title(selected_country + " Performance in " + str(selected_year) + " Olympics")
    st.table(medal_tally)


if user_menu == "Overall Analysis":
    editions = df['Year'].unique().shape[0]
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.header(editions)
    with col2:
        st.header("Hosts")
        st.header(cities)
    with col3:
        st.header("Sports")
        st.header(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.header(events)
    with col2:
        st.header("Athletes")
        st.header(athletes)
    with col3:
        st.header("Nations")
        st.header(nations)

    
    st.write("")
    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x='Edition', y='region Count')
    st.title("Participating Nations Over Time")
    st.plotly_chart(fig)

    st.write("")
    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x='Edition', y='Event Count')
    st.title("Events Over Time")
    st.plotly_chart(fig)

    st.write("")
    athlete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x='Edition', y='Name Count')
    st.title("Athletes Over Time")
    st.plotly_chart(fig)

    st.title("No. of Events over Time for Every Sport")
    fig, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int), annot=True)
    st.pyplot(fig)

    st.title("Most Successful Athletes")
    sportList = df['Sport'].unique().tolist()
    sportList.sort()
    sportList.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a Sport', sportList)
    x = helper.most_successful(df, selected_sport)
    st.table(x)

if user_menu == "Country-wise Analysis":
    st.title("Country-wise Analysis")
    country = np.unique(df['region'].dropna().values).tolist()
    country.insert(0, 'Overall')
    selected_country = st.selectbox("Select the Country", country)

    country_df = helper.country_medal_tally(df, selected_country)

    if selected_country == "Overall":
        st.subheader("Overall Medal Trend Across All Countries")
    else:
        st.subheader(f"Medal Trend for {selected_country}")

    fig = px.line(country_df, x='Year', y='Medal Count')
    st.plotly_chart(fig)

    st.title(f"Top 10 Athletes in {selected_country}")
    top_athletes = helper.top_athlete_in_country(df, selected_country)
    st.table(top_athletes)


