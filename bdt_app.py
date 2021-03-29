#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 14:56:24 2021

@author: advait_t
"""

import streamlit as st
import pandas as pd
import base64
import plotly.express as px

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(
        csv.encode()
    ).decode()  # some strings <-> bytes conversions necessary here
    return f'<a href="data:file/csv;base64,{b64}" download="dataset.csv">Download CSV file</a>'

st.title('IPL Data Extractor')
bat_data = pd.read_csv('https://raw.githubusercontent.com/advait-t/IPL_Datasets/main/Data/batting_data_IPL.csv', sep = ',')
bowl_data = pd.read_csv('https://raw.githubusercontent.com/advait-t/IPL_Datasets/main/Data/bowling_data_IPL.csv', sep=',')
player_data = pd.read_csv('https://raw.githubusercontent.com/advait-t/IPL_Datasets/main/Data/IPL_2020_Playerdataset.csv', sep=',')

data_select = st.sidebar.selectbox('Select a Dataset',['Matchwise Batting', 'Matchwise Bowling', '2020 IPL Player Data'])

if data_select == 'Matchwise Batting':
    if st.sidebar.radio('Download Raw data'): #Done
        st.subheader('Raw data')
        st.write(bat_data)
        st.markdown(get_table_download_link(bat_data), unsafe_allow_html=True)

    if st.sidebar.checkbox('Batting Data Summary'):
        summary_select = st.selectbox('Summaries', ['Most Fantasy Points Earned', 'Batting Scorecards', 'Batsmen with Highest Strike Rates','Most Sixes', 'Most Fours','Batsman Record'])
        
        if summary_select == 'Most Fantasy Points Earned': #done
            st.subheader(" Top Batsmen by Fantasy Points Earned ")
            unique_season = bat_data['Season'].unique()
            unique_season = sorted(unique_season)
            season_select = st.multiselect('Choose one or multiple seasons',unique_season)
            season_data = bat_data[(bat_data["Season"].isin(season_select))]
            nobat_to_filter = st.slider('Count of Batsmen', 0, 20, 5)
            grp_data = season_data[['Name','Fantasy_Points']]
            grp_data['Fantasy_Points'] = grp_data['Fantasy_Points'].replace(to_replace='#VALUE!', value = 0)
            grp_data['Fantasy_Points'] = grp_data['Fantasy_Points'].astype(int)
            a = pd.DataFrame(grp_data.groupby('Name')['Fantasy_Points'].sum())
            a['Name']=a.index
            a = a.nlargest(nobat_to_filter, 'Fantasy_Points')
            fig = px.bar(a, x='Name', y='Fantasy_Points', color='Fantasy_Points',labels={'Batsman': 'Batsman Name', 'Fantasy Points': 'Fantasy_Points'})
            st.plotly_chart(fig)
            st.subheader('Download Chart Data')
            st.markdown(get_table_download_link(a), unsafe_allow_html=True)
            
        elif summary_select == 'Batting Scorecards': #Done
            st.header("Season Wise Batting Scorecards")
            unique_season = bat_data['Season'].unique()
            unique_season = sorted(unique_season)
            season_select = st.multiselect('Choose one or multiple seasons',unique_season)
            season_data = bat_data[(bat_data["Season"].isin(season_select))]
            st.subheader("Download Data")
            st.write(season_data)
            st.markdown(get_table_download_link(season_data), unsafe_allow_html=True) 
            
        elif summary_select == 'Highest Strike Rate': #Done
            st.header(" Batsmen with Highest Strike Rate")
            unique_season = bat_data['Season'].unique()
            unique_season = sorted(unique_season)
            season_select = st.multiselect('Choose one or multiple seasons',unique_season)
            season_data = bat_data[(bat_data["Season"].isin(season_select))]
            nobat_to_filter = st.slider('Count of Batsmen', 0, 20, 5)
            grp_data = season_data[['Name','SR']]
            a = pd.DataFrame(grp_data.groupby('Name')['SR'].mean())
            a['Name']=a.index
            a = a.nlargest(nobat_to_filter, 'SR')
            fig = px.bar(a, x='Name', y='SR', color='SR',labels={'Batsman': 'Batsman Name', 'Strike Rate': 'SR'})
            st.plotly_chart(fig)
            st.subheader('Download Chart Data')
            st.markdown(get_table_download_link(a), unsafe_allow_html=True)
            
        elif summary_select == 'Most Sixes': #Done
            st.header(" Batsmen with most Sixes ")
            unique_season = bat_data['Season'].unique()
            unique_season = sorted(unique_season)
            season_select = st.multiselect('Choose one or multiple seasons',unique_season)
            season_data = bat_data[(bat_data["Season"].isin(season_select))]            
            nobat_to_filter = st.slider('Count of Batsmen', 0, 20, 5)
            grp_data = season_data[['Name','6s']]
            grp_data['6s'] = grp_data['6s'].replace(to_replace='-', value = 0)
            grp_data['6s'] = grp_data['6s'].astype(int)
            a = pd.DataFrame(grp_data.groupby('Name')['6s'].sum())
            a['Name']=a.index
            a = a.nlargest(nobat_to_filter, '6s')
            fig = px.bar(a, x='Name', y='6s', color='6s',labels={'Batsman': 'Batsman Name', 'Sixes': '6s'})
            st.plotly_chart(fig)
            st.subheader('Download Chart Data')
            st.markdown(get_table_download_link(a), unsafe_allow_html=True)
        
        elif  summary_select == 'Most Fours': #Done
            st.header(" Batsmen with most Fours ")
            unique_season = bat_data['Season'].unique()
            unique_season = sorted(unique_season)
            season_select = st.multiselect('Choose one or multiple seasons',unique_season)
            season_data = bat_data[(bat_data["Season"].isin(season_select))]
            nobat_to_filter = st.slider('Count of Batsmen', 0, 20, 5)
            grp_data = season_data[['Name','4s']]
            grp_data['4s'] = grp_data['4s'].replace(to_replace='-', value = 0)
            grp_data['4s'] = grp_data['4s'].astype(int)
            a = pd.DataFrame(grp_data.groupby('Name')['4s'].sum())
            a['Name']=a.index
            a = a.nlargest(nobat_to_filter, '4s')
            fig = px.bar(a, x='Name', y='4s', color='4s',labels={'Batsman': 'Batsman Name', 'Fours': '4s'})
            st.plotly_chart(fig)
            st.subheader('Download Chart Data')
            st.markdown(get_table_download_link(a), unsafe_allow_html=True)
            
        else: #Done maybe add a chart as well
            st.header('Batsman Record')
            unique_bats = bat_data['Name'].unique()
            unique_bats = sorted(unique_bats)
            a = st.multiselect('Choose one or multiple Batsmen',unique_bats)
            unique_season = bat_data['Season'].unique()
            unique_season = sorted(unique_season)
            season_select = st.multiselect('Choose one or multiple seasons',unique_season)
            season_data = bat_data[(bat_data["Season"].isin(season_select))]
            bats_data = season_data[(season_data["Name"].isin(a))]
            st.subheader("Download Data")
            st.write(bats_data)
            st.markdown(get_table_download_link(bats_data), unsafe_allow_html=True) 
            
            
                
elif data_select == 'Matchwise Bowling':
    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        load_state = st.subheader('Loading Data..')
        st.write(bowl_data)
        load_state.subheader('Loading Completed!')
        st.markdown(get_table_download_link(bowl_data), unsafe_allow_html=True)

    if st.checkbox('Batting Data Summary'):
        summary_select = st.selectbox('Summaries', ['Bowlers with highest Fantasy Points Earned', 'Season wise Bowling Scorecards', 'Bowlers with Most Wickets','Bowlers with Highest Economy', 'Bowlers with Lowest Economy','Bowlers Record'])
        
        if summary_select == 'Bowlers with highest Fantasy Points Earned':
            st.subheader(" Top Bowlers by Fantasy Points Earned ")
            nobat_to_filter = st.slider('Count of Bowlers', 0, 20, 5)
            grp_data = bowl_data.copy()
            grp_data['Name'] = 1
            k = pd.DataFrame(grp_data.groupby(['Name'], sort=False)['Fantasy_Points'].sum().rename_axis(["Batsman"]).nlargest(nobat_to_filter))
            Crime = pd.Series(k.index[:])
            Count = list(k['Batsman'][:])
            batsmen_count = pd.DataFrame(list(zip(Count,Crime)),columns=['Fantasy Points', 'Batsman'])
            fig = px.bar(batsmen_count, x='Batsman', y='Fantasy Points', color='Fantasy Points',
                         labels={'Batsman': 'Name', 'Fantasy Points': 'Fantasy_Points'})
            st.plotly_chart(fig)
            st.subheader('Download the Bar Chart Data')
            st.markdown(get_table_download_link(bat_data), unsafe_allow_html=True)
            
        elif summary_select == 'Season wise Batting Scorecards':
            st.header("Season Wise Batting Scorecards")
            unique_season = bowl_data['Season'].unique()
            unique_season = sorted(unique_season)
            #unique_season = unique_season.append('All')
            season_select = st.multiselect('Choose one or multiple seasons',unique_season)
            season_data = bat_data[(bat_data["Season"].isin(season_select))]
            st.subheader("Download Data")
            st.write(season_data)
            st.markdown(get_table_download_link(season_data), unsafe_allow_html=True) 
            
        elif summary_select == 'Batsmen with Highest Strike Rates':
            st.header(" Batsmen with Highest Strike Rates ")
            nobat_to_filter = st.slider('Count of Batsmen', 0, 20, 5)
            grp_data = bat_data.copy()
            grp_data['Fantasy_Points'] = 1
            k = pd.DataFrame(grp_data.groupby(['Fantasy_Points'], sort=False)['Fantasy_Points'].sum().rename_axis(["Batsman"]).nlargest(nobat_to_filter))
            Crime = pd.Series(k.index[:])
            Count = list(k['Fantasy_Points'][:])
            batsmen_count = pd.DataFrame(list(zip(Count,Crime)),columns=['Fantasy Points', 'Batsman'])
            fig = px.bar(batsmen_count, x='Batsman', y='Fantasy Points', color='Fantasy Points',
                         labels={'Batsman': 'Name', 'Fantasy Points': 'Fantasy_Points'})
            st.plotly_chart(fig)
            st.subheader('Download the Bar Chart Data')
            st.markdown(get_table_download_link(bat_data), unsafe_allow_html=True)
            
        elif summary_select == 'Batsmen with most Sixes':
            st.header(" Batsmen with most Sixes ")
            nobat_to_filter = st.slider('Count of Batsmen', 0, 20, 5)
            grp_data = bat_data.copy()
            grp_data['Fantasy_Points'] = 1
            k = pd.DataFrame(grp_data.groupby(['Fantasy_Points'], sort=False)['Fantasy_Points'].sum().rename_axis(["Batsman"]).nlargest(nobat_to_filter))
            Crime = pd.Series(k.index[:])
            Count = list(k['Fantasy_Points'][:])
            batsmen_count = pd.DataFrame(list(zip(Count,Crime)),columns=['Fantasy Points', 'Batsman'])
            fig = px.bar(batsmen_count, x='Batsman', y='Fantasy Points', color='Fantasy Points',
                         labels={'Batsman': 'Name', 'Fantasy Points': 'Fantasy_Points'})
            st.plotly_chart(fig)
            st.subheader('Download the Bar Chart Data')
            st.markdown(get_table_download_link(bat_data), unsafe_allow_html=True)
        
        elif  summary_select == 'Batsmen with most Fours':
            st.header(" Batsmen with most Fours ")
            nobat_to_filter = st.slider('Count of Batsmen', 0, 20, 5)
            grp_data = bat_data.copy()
            grp_data['Fantasy_Points'] = 1
            k = pd.DataFrame(grp_data.groupby(['Fantasy_Points'], sort=False)['Fantasy_Points'].sum().rename_axis(["Batsman"]).nlargest(nobat_to_filter))
            Crime = pd.Series(k.index[:])
            Count = list(k['Fantasy_Points'][:])
            batsmen_count = pd.DataFrame(list(zip(Count,Crime)),columns=['Fantasy Points', 'Batsman'])
            fig = px.bar(batsmen_count, x='Batsman', y='Fantasy Points', color='Fantasy Points',
                         labels={'Batsman': 'Name', 'Fantasy Points': 'Fantasy_Points'})
            st.plotly_chart(fig)
            st.subheader('Download the Bar Chart Data')
            st.markdown(get_table_download_link(bat_data), unsafe_allow_html=True)
            
        else:
            st.header('Batsmen Record')
            unique_bats = bat_data['Name'].unique()
            unique_bats = sorted(unique_bats)
            a = st.selectbox('Choose a Batsman',unique_bats)
            st.subheader(a)
            bats_data = pd.DataFrame(bat_data.query('Name == @a'))
            st.subheader("Download Data")
            st.write(bats_data)
            st.markdown(get_table_download_link(bats_data), unsafe_allow_html=True) 
            
else:
    st.dataframe(player_data)   
    st.markdown(get_table_download_link(player_data), unsafe_allow_html=True)
    