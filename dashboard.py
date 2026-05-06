import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("INTERNSHIP PROJECT ANALYTICS DASHBOARD")

@st.cache_data
def load_data():
    df = pd.read_csv('internship_data.csv')
    df['Start_Date'] = pd.to_datetime(df['Start_Date'])
    return df

df = load_data()

# Sidebar Filter - Idhu dhan Dynamic ah maathum
st.sidebar.header("Filter Pannu:")
departments = st.sidebar.multiselect(
    "Department Select Pannu:",
    options=df['Department'].unique(),
    default=df['Department'].unique()
)
filtered_df = df[df['Department'].isin(departments)]

# Row 1 - 2 Charts
col1, col2 = st.columns(2)
with col1:
    fig1 = px.line(filtered_df, x='Start_Date', y='Hours_Spent', title='Hours Trend Over Time')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    dept_hours = filtered_df.groupby('Department')['Hours_Spent'].sum().reset_index()
    fig2 = px.bar(dept_hours, x='Department', y='Hours_Spent', title='Total Hours by Department', text_auto=True)
    st.plotly_chart(fig2, use_container_width=True)

# Row 2 - 2 Charts  
col3, col4 = st.columns(2)
with col3:
    fig3 = px.scatter(filtered_df, x='Team_Members', y='Hours_Spent', color='Status', title='Team Size vs Hours Spent')
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    status_count = filtered_df['Status'].value_counts()
    fig4 = px.pie(status_count, names=status_count.index, values=status_count.values, title='Project Status Distribution')
    st.plotly_chart(fig4, use_container_width=True)

st.subheader("Filtered Data Table")
st.dataframe(filtered_df)
