#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 14:56:24 2021

@author: advait_t
"""

import streamlit as st
import pandas as pd
import base64
import plotly.express as pxx

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

@st.cache 
def download_data(l1,l2,l3):
    bat_data = pd.read_csv(l1, sep = ',')
    bowl_data = pd.read_csv(l2, sep=',')
    player_data = pd.read_csv(l3, sep=',')
    return bat_data, bowl_data, player_data


    

def home():
    st.title("IPL Data Extractor")
    st.write("A data extration tool to extract IPL data and let the user download CSV files using simple queries on batting and bowling scorecards as well as IPL 2020 squad data.")
    

def multi_select_box_bat(df):
    unique_season = df['Season'].unique()
    unique_season = sorted(unique_season)
    container = st.beta_container()
    all_season = st.checkbox("Select all Seasons")
    if all_season:
        season_select = container.multiselect('Choose one or multiple seasons',unique_season,unique_season)
    else:
        season_select = container.multiselect('Choose one or multiple seasons',unique_season)
    season_data = df[(df["Season"].isin(season_select))]
    unique_team = season_data['Teams'].unique()
    unique_team = sorted(unique_team)
    container1 = st.beta_container()
    all_team = st.checkbox("Select all Teams")
    if all_team:
        team_select = container1.multiselect('Choose one or multiple teams',unique_team,unique_team)
    else:
        team_select = container1.multiselect('Choose one or multiple teams',unique_team)
    team_data = season_data[(season_data["Teams"].isin(team_select))]
    return(team_data)
    
def multi_select_box_player(df):
    unique_team = df['Team'].unique()
    unique_team = sorted(unique_team)
    container1 = st.beta_container()
    all_team = st.checkbox("Select all Teams")
    if all_team:
        team_select = container1.multiselect('Choose one or multiple teams',unique_team,unique_team)
    else:
        team_select = container1.multiselect('Choose one or multiple teams',unique_team)
    team_data = df[(df["Team"].isin(team_select))]
    
    unique_nationality = df['Nationality'].unique()
    unique_nationality = sorted(unique_nationality)
    container = st.beta_container()
    all_season = st.checkbox("Select all Nationalities")
    if all_season:
        nation_select = container.multiselect('Choose one or multiple Nationalities',unique_nationality,unique_nationality)
    else:
        nation_select = container.multiselect('Choose one or multiple Nationalities',unique_nationality)
    nation_data = team_data[(team_data["Nationality"].isin(nation_select))]
    return(nation_data)
    
def player(data,col):
    grp_data = data[['Name',col]]
    nobat_to_filter = st.slider('Count of Players', 0, 20, 5)
    grp_data[col] = grp_data[col].fillna(0)
    grp_data[col] = grp_data[col].astype(float)
    grp_data = grp_data.nlargest(nobat_to_filter, col)
    fig = px.bar(grp_data, x='Name', y=col, color=col)
    return fig, grp_data
        
def bdt_app(bat_data,bowl_data,player_data):
    st.title('IPL Data Extractor')
    data_select = st.sidebar.selectbox('Select a Dataset',['Batting', 'Bowling', '2020 IPL Player Data'])
    
    if data_select == 'Batting':
        radio = st.sidebar.radio('Select type to download data',['Download Raw Batting Data','Download by Query','Download by Custom Query'])
        if radio == 'Download Raw Batting Data': #Done
            st.subheader('Raw data')
            st.write(bat_data)
            st.markdown(get_table_download_link(bat_data), unsafe_allow_html=True)
    
        elif radio == 'Download by Query':
            summary_select = st.selectbox('Summaries', ['Most Fantasy Points Earned', 'Batting Scorecards', 'Highest Strike Rate','Most Sixes', 'Most Fours','Batsman Record'])
            if summary_select == 'Most Fantasy Points Earned': #done
                st.subheader(" Top Batsmen by Fantasy Points Earned ")
                
                team_data = multi_select_box_bat(bat_data)
                
                nobat_to_filter = st.slider('Count of Batsmen', 0, 20, 5)
                grp_data = team_data[['Player','Fantasy_Points']]
                grp_data['Fantasy_Points'] = grp_data['Fantasy_Points'].replace(to_replace='#VALUE!', value = 0)
                grp_data['Fantasy_Points'] = grp_data['Fantasy_Points'].astype(int)
                a = pd.DataFrame(grp_data.groupby('Player')['Fantasy_Points'].sum())
                a['Player']=a.index
                a = a.nlargest(nobat_to_filter, 'Fantasy_Points')
                fig = pxx.bar(a, x='Player', y='Fantasy_Points', color='Fantasy_Points',labels={'Batsman': 'Batsman Name', 'Fantasy Points': 'Fantasy_Points'})
                st.plotly_chart(fig)
                st.subheader('Download Chart Data')
                st.markdown(get_table_download_link(a), unsafe_allow_html=True)
                
            elif summary_select == 'Batting Scorecards': #Done
                st.header("Season Wise Batting Scorecards")
                
                team_data = multi_select_box_bat(bat_data)
                
                st.subheader("Download Data")
                st.write(team_data)
                st.markdown(get_table_download_link(team_data), unsafe_allow_html=True) 
                
            elif summary_select == 'Highest Strike Rate': #Done
                st.header("Batsmen with Highest Strike Rate")
                
                team_data = multi_select_box_bat(bat_data)
                
                nobat_to_filter = st.slider('Count of Batsmen', 0, 20, 5)
                grp_data = team_data[['Player','SR']]
                a = pd.DataFrame(grp_data.groupby('Player')['SR'].mean())
                a['Player']=a.index
                a = a.nlargest(nobat_to_filter, 'SR')
                fig = pxx.bar(a, x='Player', y='SR', color='SR',labels={'Batsman': 'Batsman Name', 'Strike Rate': 'Strike Rate'})
                st.plotly_chart(fig)
                st.subheader('Download Chart Data')
                st.markdown(get_table_download_link(a), unsafe_allow_html=True)
                
            elif summary_select == 'Most Sixes': #Done
                st.header(" Batsmen with most Sixes ")
                
                team_data = multi_select_box_bat(bat_data)
                
                nobat_to_filter = st.slider('Count of Batsmen', 0, 20, 5)
                
                grp_data = team_data[['Player','6s']]
                grp_data['6s'] = grp_data['6s'].replace(to_replace='-', value = 0)
                grp_data['6s'] = grp_data['6s'].astype(int)
                a = pd.DataFrame(grp_data.groupby('Player')['6s'].sum())
                a['Player']=a.index
                a = a.nlargest(nobat_to_filter, '6s')
                fig = pxx.bar(a, x='Player', y='6s', color='6s',labels={'Batsman': 'Batsman Name', 'Sixes': '6s'})
                st.plotly_chart(fig)
                st.subheader('Download Chart Data')
                st.markdown(get_table_download_link(a), unsafe_allow_html=True)
            
            elif  summary_select == 'Most Fours': #Done
                st.header(" Batsmen with most Fours ")
    
                team_data = multi_select_box_bat(bat_data)
    
                nobat_to_filter = st.slider('Count of Batsmen', 0, 20, 5)
                grp_data = team_data[['Player','4s']]
                grp_data['4s'] = grp_data['4s'].replace(to_replace='-', value = 0)
                grp_data['4s'] = grp_data['4s'].astype(int)
                a = pd.DataFrame(grp_data.groupby('Player')['4s'].sum())
                a['Player']=a.index
                a = a.nlargest(nobat_to_filter, '4s')
                fig = pxx.bar(a, x='Player', y='4s', color='4s',labels={'Batsman': 'Batsman Name', 'Fours': '4s'})
                st.plotly_chart(fig)
                st.subheader('Download Chart Data')
                st.markdown(get_table_download_link(a), unsafe_allow_html=True)
                
            else: #Done maybe add a chart as well
                st.header('Batsman Record')
                unique_season = bat_data['Season'].unique()
                unique_season = sorted(unique_season)
                container = st.beta_container()
                all_season = st.checkbox("Select all Seasons")
                if all_season:
                    season_select = container.multiselect('Choose one or multiple seasons',unique_season,unique_season)
                else:
                    season_select = container.multiselect('Choose one or multiple seasons',unique_season)
                    
                season_data = bat_data[(bat_data["Season"].isin(season_select))]
                
                unique_player = season_data['Player'].unique()
                unique_player = sorted(unique_player)
                container1 = st.beta_container()
                all_players = st.checkbox("Select all Players")
                if all_players:
                    player_select = container1.multiselect('Choose one or multiple players',unique_player,unique_player)
                else:
                    player_select = container1.multiselect('Choose one or multiple players',unique_player)
                
                player_data = season_data[(season_data["Player"].isin(player_select))]
                
                unique_team = player_data['Teams'].unique()
                unique_team = sorted(unique_team)
                container2 = st.beta_container()
                all_teams = st.checkbox("Select all Teams")
                if all_teams:
                    team_select = container2.multiselect('Choose one or multiple teams',unique_team,unique_team)
                else:
                    team_select = container2.multiselect('Choose one or multiple teams',unique_team)
                
                team_data = player_data[(player_data["Teams"].isin(team_select))]
            
                
                st.subheader("Download Data")
                st.write(team_data)
                st.markdown(get_table_download_link(team_data), unsafe_allow_html=True)
        else:
            st.header('This page will be active soon...')
            
            
                
                
                    
    elif data_select == 'Bowling':
        radio = st.sidebar.radio('Select type to download data',['Download Raw Bowling Data','Download by Query','Download by Custom Query'])
        if radio == 'Download Raw Bowling Data': #Done
            st.subheader('Raw data')
            st.write(bowl_data)
            st.markdown(get_table_download_link(bowl_data), unsafe_allow_html=True)
    
        elif radio == 'Download by Query':
            summary_select = st.selectbox('Summaries', ['Most Fantasy Points Earned', 'Bowling Scorecards', 'Most Wickets Taken','Most Sixes Conceded', 'Most Fours Conceded','Bowler Record', 'Best Economy Rate'])
            if summary_select == 'Most Fantasy Points Earned': #done
                st.subheader(" Top Bowlers by Fantasy Points Earned ")
                
                team_data = multi_select_box_bat(bowl_data)
                
                nobat_to_filter = st.slider('Count of Bowlers', 0, 20, 5)
                grp_data = team_data[['Player','Fantasy_Points']]
                grp_data['Fantasy_Points'] = grp_data['Fantasy_Points'].replace(to_replace='#VALUE!', value = 0)
                grp_data['Fantasy_Points'] = grp_data['Fantasy_Points'].astype(int)
                a = pd.DataFrame(grp_data.groupby('Player')['Fantasy_Points'].sum())
                a['Player']=a.index
                a = a.nlargest(nobat_to_filter, 'Fantasy_Points')
                fig = pxx.bar(a, x='Player', y='Fantasy_Points', color='Fantasy_Points',labels={'Bowler': 'Bowler Name', 'Fantasy Points': 'Fantasy_Points'})
                st.plotly_chart(fig)
                st.subheader('Download Chart Data')
                st.markdown(get_table_download_link(a), unsafe_allow_html=True)
                
            elif summary_select == 'Bowling Scorecards': #Done
                st.header("Season Wise Bowling Scorecards")
                team_data = multi_select_box_bat(bowl_data)
                st.subheader("Download Data")
                st.write(team_data)
                st.markdown(get_table_download_link(team_data), unsafe_allow_html=True) 
                
            elif summary_select == 'Most Wickets Taken': #Done
                st.header("Bowlers with Most Wickets")
                team_data = multi_select_box_bat(bowl_data)
                nobat_to_filter = st.slider('Count of Bowlers', 0, 20, 5)
                grp_data = team_data[['Player','Wickets']]
                a = pd.DataFrame(grp_data.groupby('Name')['Wickets'].sum())
                a['Player']=a.index
                a = a.nlargest(nobat_to_filter, 'Wickets')
                fig = pxx.bar(a, x='Player', y='Wickets', color='Wickets',labels={'Bowler': 'Bowler Name', 'Wickets': 'Wickets'})
                st.plotly_chart(fig)
                st.subheader('Download Chart Data')
                st.markdown(get_table_download_link(a), unsafe_allow_html=True)
                
            elif summary_select == 'Most Sixes Conceded': #Done
                st.header(" Bowlers giving most Sixes ")
                team_data = multi_select_box_bat(bowl_data)       
                nobat_to_filter = st.slider('Count of Bowlers', 0, 20, 5)
                grp_data = team_data[['Player','6s']]
                grp_data['6s'] = grp_data['6s'].replace(to_replace='-', value = 0)
                grp_data['6s'] = grp_data['6s'].astype(int)
                a = pd.DataFrame(grp_data.groupby('Player')['6s'].sum())
                a['Player']=a.index
                a = a.nlargest(nobat_to_filter, '6s')
                fig = pxx.bar(a, x='Player', y='6s', color='6s',labels={'Bowler': 'Bowler Name', 'Sixes': '6s'})
                st.plotly_chart(fig)
                st.subheader('Download Chart Data')
                st.markdown(get_table_download_link(a), unsafe_allow_html=True)
            
            elif  summary_select == 'Most Fours Conceded': #Done
                st.header(" Bowlers giving most Fours ")
                team_data = multi_select_box_bat(bowl_data)
                nobat_to_filter = st.slider('Count of Bowlers', 0, 20, 5)
                grp_data = team_data[['Player','4s']]
                grp_data['4s'] = grp_data['4s'].replace(to_replace='-', value = 0)
                grp_data['4s'] = grp_data['4s'].astype(int)
                a = pd.DataFrame(grp_data.groupby('Player')['4s'].sum())
                a['Player']=a.index
                a = a.nlargest(nobat_to_filter, '4s')
                fig = pxx.bar(a, x='Player', y='4s', color='4s',labels={'Bowler': 'Bowler Name', 'Fours': '4s'})
                st.plotly_chart(fig)
                st.subheader('Download Chart Data')
                st.markdown(get_table_download_link(a), unsafe_allow_html=True)
                
            elif summary_select == 'Best Economy Rate':
                st.header(" Bowlers with Best Economy Rate")
                team_data = multi_select_box_bat(bowl_data)
                nobat_to_filter = st.slider('Count of Bowlers', 0, 20, 5)
                grp_data = team_data[['Player','Econ']]
                a = pd.DataFrame(grp_data.groupby('Name')['Econ'].mean())
                a['Player']=a.index
                a = a.nsmallest(nobat_to_filter, 'Econ')
                fig = pxx.bar(a, x='Player', y='Econ', color='Econ',labels={'Bowler': 'Bowler Name', 'Economy Rate': 'Economy Rate'})
                st.plotly_chart(fig)
                st.subheader('Download Chart Data')
                st.markdown(get_table_download_link(a), unsafe_allow_html=True)
                
            else: #Done maybe add a chart as well
                st.header('Bowler Record')
                unique_season = bowl_data['Season'].unique()
                unique_season = sorted(unique_season)
                container = st.beta_container()
                all_season = st.checkbox("Select all Seasons")
                if all_season:
                    season_select = container.multiselect('Choose one or multiple seasons',unique_season,unique_season)
                else:
                    season_select = container.multiselect('Choose one or multiple seasons',unique_season)
                    
                season_data = bowl_data[(bowl_data["Season"].isin(season_select))]
                
                unique_player = season_data['Player'].unique()
                unique_player = sorted(unique_player)
                container1 = st.beta_container()
                all_players = st.checkbox("Select all Players")
                if all_players:
                    player_select = container1.multiselect('Choose one or multiple players',unique_player,unique_player)
                else:
                    player_select = container1.multiselect('Choose one or multiple players',unique_player)
                
                player_data = season_data[(season_data["Player"].isin(player_select))]
                
                unique_team = player_data['Teams'].unique()
                unique_team = sorted(unique_team)
                container2 = st.beta_container()
                all_teams = st.checkbox("Select all Teams")
                if all_teams:
                    team_select = container2.multiselect('Choose one or multiple teams',unique_team,unique_team)
                else:
                    team_select = container2.multiselect('Choose one or multiple teams',unique_team)
                
                team_data = player_data[(player_data["Teams"].isin(team_select))]
            
                
                st.subheader("Download Data")
                st.write(team_data)
                if st.button('Download Data'):
                    st.markdown(get_table_download_link(team_data), unsafe_allow_html=True)
        else:
            st.header('This page will be active soon...')
                    
                
    elif data_select == '2020 IPL Player Data':
        radio = st.sidebar.radio('Select type to download data',['Download Raw 2020 Squad Data','Download by Pre-Defined Queries','Download by Custom Query'])
        if radio == 'Download Raw 2020 Squad Data':
            st.subheader('Raw data')
            st.write(player_data)   
            st.markdown(get_table_download_link(player_data), unsafe_allow_html=True)
        elif radio == 'Download by Pre-Defined Queries':
            summary_select = st.selectbox('Query', ['Players by Nationality', 'Most Matches Played', 'Wickets Taken by Bowlers','Best Economy Rate', 'Most Runs Scored','Best Strike Rate'])
            if summary_select == 'Players by Nationality':
                data = multi_select_box_player(player_data)
                st.write(data)
                st.markdown(get_table_download_link(data), unsafe_allow_html=True)
                
            elif summary_select == 'Most Matches Played':
                data = multi_select_box_player(player_data)
                fig, grp_data = player(data,'Matches')
                st.plotly_chart(fig)
                st.subheader('Download Chart Data')
                st.markdown(get_table_download_link(grp_data), unsafe_allow_html=True)
                
            elif summary_select == 'Wickets Taken by Bowlers':
                data = multi_select_box_player(player_data)
                fig, grp_data = player(data,'Bowl-Wickets')
                st.plotly_chart(fig)
                st.subheader('Download Chart Data')
                st.markdown(get_table_download_link(grp_data), unsafe_allow_html=True)
                
            elif summary_select == 'Best Economy Rate':
                data = multi_select_box_player(player_data)
                fig, grp_data = player(data,'Bowl-Economy')
                st.plotly_chart(fig)
                st.subheader('Download Chart Data')
                st.markdown(get_table_download_link(grp_data), unsafe_allow_html=True)
                
            elif summary_select == 'Most Runs Scored':
                data = multi_select_box_player(player_data)
                fig, grp_data = player(data,'Bat-Runs')
                st.plotly_chart(fig)
                st.subheader('Download Chart Data')
                st.markdown(get_table_download_link(grp_data), unsafe_allow_html=True)
            
            else:
                data = multi_select_box_player(player_data)
                fig, grp_data = player(data,'Bat-Strike Rate')
                st.plotly_chart(fig)
                st.subheader('Download Chart Data')
                st.markdown(get_table_download_link(grp_data), unsafe_allow_html=True)
        else:
            st.header('This page will be active soon...')
            
    
bat_data, bowl_data, player_data = download_data('https://raw.githubusercontent.com/advait-t/IPL_Datasets/main/Data/batting_data.csv','https://raw.githubusercontent.com/advait-t/IPL_Datasets/main/Data/bowling_data.csv','https://raw.githubusercontent.com/advait-t/IPL_Datasets/main/Data/IPL_2020_Playerdataset.csv')
st.sidebar.title('IPL Data Extractor')
option_select = st.sidebar.radio('Select an Option',['About Us','Data Extractor'])
if option_select == 'About Us':
    home()
else:
    bdt_app(bat_data,bowl_data,player_data)