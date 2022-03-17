import pandas as pd
import streamlit as st

df = pd.read_csv('data/full_table_v0.4.csv', index_col=0)

# Title
st.title('Restaurant Dashboard')

# Page 1
st.subheader('General Insights')

# New York
st.markdown('**New York**')
col1, col2, col3 = st.columns(3)
col1.metric(label='Aggregate Orders',
            value=df.groupby('city')['order_id'].nunique()['New York'])
col2.metric(label='Unique Customers',
            value=df.groupby('city')['customer_id'].nunique()['New York'])
col3.metric(label='Total Revenue',
            value=df.groupby('city')['revenue'].sum()['New York'].round(0))

# San Francisco
st.markdown('**San Francisco**')
col1, col2, col3 = st.columns(3)
col1.metric(label='Aggregate Orders',
            value=df.groupby('city')['order_id'].nunique()['San Francisco'])
col2.metric(label='Unique Customers',
            value=df.groupby('city')['customer_id'].nunique()['San Francisco'])
col3.metric(
    label='Total Revenue',
    value=df.groupby('city')['revenue'].sum()['San Francisco'].round(0))

# Favourite dish
st.markdown('**Favourite Dish**')
st.markdown(
    f'**New York**: {df.groupby("city")["dish_name"].max()["New York"]}')
st.markdown(
    f'**San Francisco**: {df.groupby("city")["dish_name"].max()["San Francisco"]}'
)

# Favourite Restaurant
st.markdown('**Favourite Restaurant**')
st.markdown(
    f'**New York**: {df.groupby("city")["rest_name"].max()["New York"]}')
st.markdown(
    f'**San Francisco**: {df.groupby("city")["rest_name"].max()["San Francisco"]}'
)