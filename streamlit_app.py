import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import datetime as datetime

st.title('African Covid Report analysis')
st.sidebar.title('African Covi Report analysis')


#st.image('https://issafrica.s3.amazonaws.com/site/images/banners/2020-05-14-iss-today-africa-covid-strat-banner.jpg', width =400)

st.markdown('🦠This application is a streamlit Dashbord to analyze some aspects of Covid-19 Spread on the African continent🦠')
st.sidebar.markdown('🦠This application is a streamlit Dashbord to analyze some aspects of Covid-19 Spread on the African continent🦠')

DATA_URL = ('african_covid_report_last.csv')  
DATA_URL_2 =('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv')


@st.cache(persist=False)
def load_data():
    data = pd.read_csv(DATA_URL)
    #data = data.groupby(['date', 'country', 'region', 'iso_alpha'])[['confirmed', 'deaths', 'recovered','active', 'new_confirmed', 'new_deaths', 'new_recovered','population']].sum().reset_index()
    return data
data = load_data()


def load_data_2():
    data2 = pd.read_csv(DATA_URL_2)
    data2 = data2.groupby(['date', 'location', 'iso_code', 'continent']).sum().reset_index()
    return data2
data2 = load_data_2()

#output the global stats of continent
stats_count = data.groupby(['date'])['confirmed', 'deaths', 'recovered'].sum().reset_index()

stats_count = stats_count[stats_count['date']==max(stats_count['date'])]
africa_confirmed = stats_count["confirmed"].max().astype(int)
africa_deaths = stats_count['deaths'].max().astype(int)
affrica_recovered = stats_count['recovered'].max().astype(int)
stats_count['date'] = pd.to_datetime(stats_count['date'], infer_datetime_format=True)
day = stats_count['date'].max()
day = day.strftime('%B %d, %Y')
stats_count_string = f'{day} Africa count : \n -  `{africa_confirmed:,d}` Confirmed \n - `{africa_deaths:,d}` Deaths \n  - `{affrica_recovered:,d}` Recovered.'
stats = st.markdown(stats_count_string)

#output the highest confirmed case country
higher_rate = data.groupby(['country'])['confirmed'].max().reset_index().sort_values('confirmed', ascending=False)
higher_rate = higher_rate.reset_index(drop=True)
country_name = higher_rate['country'][0]
high_confirmed = higher_rate['confirmed'][0]


hcfst = f'`{country_name}` is the most infected country with `{high_confirmed:,d}` cases'
high_country_rate = st.subheader('Confirmed cases')
high_stats = st.markdown(hcfst)

#output the highest deaths cases country
higher_deaths = data.groupby(['country'])['deaths'].max().reset_index().sort_values('deaths', ascending=False)
higher_deaths = higher_deaths.reset_index(drop=True)
country_deaths_name = higher_deaths['country'][0]
deaths_cases = higher_deaths['deaths'][0]
deaths_string = f'`{country_deaths_name}` as the highest deaths number with `{deaths_cases:,d}`'
deaths_header = st.subheader('Deaths')
stats_deaths = st.markdown(deaths_string)



st.markdown('---')
st.sidebar.markdown('---')
st.sidebar.markdown('Mapping of Covid 19 spread')
map_selector = st.sidebar.selectbox('Choose a map', ['African Bubble Map', 'World Bubble Map'], key = '1')

df_maps = data.groupby(['date', 'country', 'iso_alpha', 'region']).sum().reset_index()
df_maps = df_maps[df_maps.date >='2020-02-25']
if not st.sidebar.checkbox('Hide', True):
    st.subheader('Mapping of COvid 19 spread')
    if map_selector == 'African Bubble Map':
        fig = px.scatter_geo(df_maps, locations='iso_alpha', animation_frame='date', color='region', size='confirmed', size_max=60, scope='africa',
                             hover_data=['confirmed', 'deaths', 'recovered', 'active'], hover_name='country')
        fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration']=2
        fig.update_layout(title= 'Evolution cases of Covid-19 in Africa', height = 500 )
        st.plotly_chart(fig)
        comment = st.markdown("This map shows the evolution infections on the continent. We note that South Africa is the country with the most infections.")
    else :
        fig = px.scatter_geo(data2, locations='iso_code', animation_frame='date', color='continent', size='total_cases', 
                             hover_data=['total_cases', 'total_deaths'], hover_name='location', size_max=60, projection='natural earth', height=500)
        fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration']=2
        fig.update_layout(title='Evolution of Covid-19 in the world')
        st.plotly_chart(fig)
        comment = st.markdown("On this map we can see that the contamination "
                              "in Africa started after the other continents, except for Oceania." 
                              "We can also see that Africa has fewer cases of contamination than other continents.")   

df_scatter = df_maps[df_maps.date>='2020-03-10']


