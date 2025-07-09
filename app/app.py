import streamlit as st
import pandas as pd
import preprocessor
import helper

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