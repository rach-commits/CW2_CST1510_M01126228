import streamlit as st
import pandas as pd
from app_model.cyber_incidents import get_all_cyber_incidents
from app_model.db import get_connection

st.set_page_config(
    page_title='Cyber Incident Dashboard',
    page_icon='👾',
    layout='wide')

conn=get_connection()
data = get_all_cyber_incidents(conn)
st.title('Welcome to the Cyber Incident Dashboard')

with st.sidebar:
    st.header('Navigation')
    severity_= st.selectbox('Severity Level', data['severity'].unique())


data['timestamp'] = pd.to_datetime(data['timestamp'])
filtered_data = data[data['severity'] == severity_]

col1, col2 = st.columns(2)
with col1:

    st.subheader(f'Cyber Incidents with Severity: {severity_}')
    st.bar_chart(filtered_data['category'].value_counts())

with col2:
    st.header('Categatory Trend Over Time')
    st.line_chart(filtered_data, x= 'timestamp', y='category')

st.subheader("Filtered Data")
st.dataframe(filtered_data)