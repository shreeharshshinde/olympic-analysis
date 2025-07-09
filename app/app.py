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


