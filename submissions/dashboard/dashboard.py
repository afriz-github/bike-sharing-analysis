import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


df = pd.read_csv("all_data.csv")
relevant_columns = ['dteday_x', 'season_x', 'weathersit_x', 'temp_x', 'hum_x', 'windspeed_x', 'cnt_x', 'hr']
df = df[relevant_columns]
df['dteday_x'] = pd.to_datetime(df['dteday_x'])


daily_df = df.groupby('dteday_x').agg({
    'season_x': 'first',
    'weathersit_x': 'first',
    'temp_x': 'mean',
    'hum_x': 'mean',
    'windspeed_x': 'mean',
    'cnt_x': 'sum'
}).reset_index()
daily_df.columns = ['date', 'season', 'weather', 'temp', 'hum', 'windspeed', 'cnt']
season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
weather_mapping = {1: 'Clear', 2: 'Cloudy', 3: 'Rainy', 4: 'Snowy'}
daily_df['season'] = daily_df['season'].map(season_mapping)
daily_df['weather'] = daily_df['weather'].map(weather_mapping)
daily_df['month_name'] = daily_df['date'].dt.month_name()


st.title('Bike Sharing Dataset Dashboard')

with st.sidebar:
    st.image("rentalbike.jpg")
    min_date = daily_df['date'].min()
    max_date = daily_df['date'].max()
    start_date, end_date = st.date_input('Date Range', min_value=min_date, max_value=max_date, value=[min_date, max_date])
    weather_options = st.multiselect('Select Weather', options=daily_df['weather'].unique(), default=daily_df['weather'].unique())
    season_options = st.multiselect('Select Season', options=daily_df['season'].unique(), default=daily_df['season'].unique())
    month_options = st.multiselect('Select Month', options=daily_df['month_name'].unique(), default=daily_df['month_name'].unique())

start_date_dt = pd.to_datetime(start_date)
end_date_dt = pd.to_datetime(end_date)
filtered_df = daily_df[(daily_df['date'].dt.date >= start_date) & (daily_df['date'].dt.date <= end_date) &
                       daily_df['weather'].isin(weather_options) &
                       daily_df['season'].isin(season_options) &
                       daily_df['month_name'].isin(month_options)]


st.subheader('Summary')
col1, col2 = st.columns(2)
with col1:
    total_rentals = filtered_df['cnt'].sum()
    st.metric("Total Rentals", value=total_rentals)
with col2:
    average_daily_rentals = round(filtered_df['cnt'].mean(), 2)
    st.metric("Average Daily Rentals", value=average_daily_rentals)
max_rental_day = filtered_df.loc[filtered_df['cnt'].idxmax(), 'date'].strftime('%Y-%m-%d')
max_rentals = filtered_df['cnt'].max()
min_rental_day = filtered_df.loc[filtered_df['cnt'].idxmin(), 'date'].strftime('%Y-%m-%d')
min_rentals = filtered_df['cnt'].min()
st.write(f"Maximum Daily Rentals: {max_rentals} on {max_rental_day}")
st.write(f"Minimum Daily Rentals: {min_rentals} on {min_rental_day}")


st.subheader('Daily Rentals Trend')
fig, ax = plt.subplots()
ax.plot(filtered_df['date'], filtered_df['cnt'], marker='o', linewidth=2, color="#90CAF9")
ax.set_title('Daily Rentals Over Time')
ax.set_xlabel('Date')
ax.set_ylabel('Number of Rentals')
plt.setp(ax.get_xticklabels(), rotation=45)
st.pyplot(fig)

st.subheader('Monthly Average Rentals')
monthly_avg = filtered_df.groupby('month_name')['cnt'].mean().reset_index()
fig, ax = plt.subplots(figsize=(10, 6))  
ax.bar(monthly_avg['month_name'], monthly_avg['cnt'])
ax.set_title('Average Rentals per Month')
ax.set_xlabel('Month')
ax.set_ylabel('Average Rentals')
plt.setp(ax.get_xticklabels(), rotation=45)  
st.pyplot(fig)


st.subheader('Weather Impact')
weather_avg = filtered_df.groupby('weather')['cnt'].mean().reset_index()
fig, ax = plt.subplots()
ax.bar(weather_avg['weather'], weather_avg['cnt'])
ax.set_title('Average Rentals by Weather')
ax.set_xlabel('Weather')
ax.set_ylabel('Average Rentals')
st.pyplot(fig)
fig, ax = plt.subplots()
ax.scatter(filtered_df['temp'], filtered_df['cnt'], color='#90CAF9')
ax.set_title('Temperature vs. Rentals')
ax.set_xlabel('Temperature')
ax.set_ylabel('Rentals')
st.pyplot(fig)
fig, ax = plt.subplots()
ax.scatter(filtered_df['hum'], filtered_df['cnt'], color='#90CAF9')
ax.set_title('Humidity vs. Rentals')
ax.set_xlabel('Humidity')
ax.set_ylabel('Rentals')
st.pyplot(fig)
fig, ax = plt.subplots()
ax.scatter(filtered_df['windspeed'], filtered_df['cnt'], color='#90CAF9')
ax.set_title('Wind Speed vs. Rentals')
ax.set_xlabel('Wind Speed')
ax.set_ylabel('Rentals')
st.pyplot(fig)


st.subheader('Seasonal Impact')
season_avg = filtered_df.groupby('season')['cnt'].mean().reset_index()
fig, ax = plt.subplots()
ax.bar(season_avg['season'], season_avg['cnt'])
ax.set_title('Average Rentals by Season')
ax.set_xlabel('Season')
ax.set_ylabel('Average Rentals')
st.pyplot(fig)


st.subheader('Correlation Heatmap')
corr_df = filtered_df[['temp', 'hum', 'windspeed', 'cnt']]
corr_matrix = corr_df.corr()
fig, ax = plt.subplots()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
st.pyplot(fig)


st.subheader('Top and Bottom Rental Days')
top_days = filtered_df.sort_values(by='cnt', ascending=False).head(5)
bottom_days = filtered_df.sort_values(by='cnt', ascending=True).head(5)
st.write('Top 5 Days:')
st.dataframe(top_days[['date', 'cnt', 'weather', 'season']])
st.write('Bottom 5 Days:')
st.dataframe(bottom_days[['date', 'cnt', 'weather', 'season']])

st.caption('Copyright (c) Aa Afriz 2025')
