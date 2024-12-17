import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data
@st.cache
def load_data():
    # Gantilah 'movies_data.csv' dengan file data Anda
    return pd.read_csv('movies_data.csv')

data = load_data()

# Preprocess data
data['budget_x'] = pd.to_numeric(data['budget_x'], errors='coerce')
data['revenue'] = pd.to_numeric(data['revenue'], errors='coerce')
data['score'] = pd.to_numeric(data['score'], errors='coerce')
data['date_x'] = pd.to_datetime(data['date_x'], errors='coerce')

# Streamlit UI controls
st.title('Interactive Movie Analytics Dashboard')

# Filter Controls
genre = st.selectbox("Filter Genre:", ['All Genres', 'Action', 'Drama', 'Comedy', 'Adventure'])
max_year = st.slider('Max Release Year:', min_value=2000, max_value=2020, value=2020)
country = st.selectbox('Production Country:', ['All Countries'] + data['country'].unique().tolist())
search_term = st.text_input('Find Movie:', '')
sort_by = st.selectbox('Sort Movies By:', ['Total Revenue', 'Audience Rating'])

# Filter data based on user input
filtered_data = data[
    (data['date_x'].dt.year <= max_year) &
    (data['genre'].isin([genre, 'All Genres']) if genre != 'All Genres' else True) &
    (data['country'].isin([country, 'All Countries']) if country != 'All Countries' else True) &
    (data['names'].str.contains(search_term, case=False) if search_term else True)
]

# Sort data
if sort_by == 'Total Revenue':
    filtered_data = filtered_data.sort_values(by='revenue', ascending=False)
else:
    filtered_data = filtered_data.sort_values(by='score', ascending=False)

# Budget vs Revenue Bubble Chart
st.subheader("Budget vs Revenue Bubble Chart")
if not filtered_data.empty:
    fig = px.scatter(
        filtered_data,
        x='budget_x',
        y='revenue',
        size='revenue',
        color='genre',
        hover_name='names',
        hover_data=['revenue', 'budget_x', 'score', 'country'],
        log_x=True,
        title="Budget vs Revenue"
    )
    st.plotly_chart(fig)
else:
    st.write("No movies found matching your search criteria.")

# Annual Movie Revenue Trend Line Chart
st.subheader("Annual Movie Revenue Trend")
if not filtered_data.empty:
    yearly_data = filtered_data.groupby(filtered_data['date_x'].dt.year)['revenue'].sum().reset_index()
    fig = px.line(
        yearly_data,
        x='date_x',
        y='revenue',
        title="Total Annual Movie Revenue"
    )
    st.plotly_chart(fig)

# Movie Status Distribution Bar Chart
st.subheader("Movie Status Distribution")
if not filtered_data.empty:
    status_data = filtered_data['status'].value_counts().reset_index()
    status_data.columns = ['Status', 'Count']
    fig = px.bar(
        status_data,
        x='Status',
        y='Count',
        title="Movie Status Distribution",
        color='Status',
        labels={'Count': 'Number of Movies'}
    )
    st.plotly_chart(fig)

# Footer
st.write("Interactive Movie Analytics Dashboard")
