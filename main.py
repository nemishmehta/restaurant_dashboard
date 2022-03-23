import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px


restaurant_df = pd.read_csv('./data/ODL_RESTAURANT.csv')
order_df = pd.read_csv('./data/ODL_ORDER.csv')
orderItem_df = pd.read_csv('./data/ODL_ORDER_ITEM.csv')
orderables_df = pd.read_csv('./data/ODL_ORDERABLES.csv')

final_df = pd.DataFrame

def get_bestseller_fig(restaurant_name:str) -> px.scatter:

    # Rename id columns for merging dataframes
    restaurant_df.rename(columns={"id":"restaurant_id"},inplace=True)
    orderables_df.rename(columns={"id":"orderable_id"},inplace=True)
    orderables_df.rename(columns={"name":"product_name"},inplace=True)

    # Merging dataframes
    rest_order_df = pd.merge(restaurant_df[['name','restaurant_id','city']], order_df, how="inner", on="restaurant_id")
    rest_order_df.rename(columns={"id":"order_id"},inplace=True)
    restorder_item_df = pd.merge(rest_order_df, orderItem_df[['order_id', 'amount', 'orderable_id']], how='inner', on='order_id')
    restorderitem_orderable_df = pd.merge(restorder_item_df,orderables_df[['price','orderable_id','product_name',]], how='inner', on='orderable_id')

    # Split creation_date as order date and order time
    data_columns = restorderitem_orderable_df['creation_date'].str.split(" ", n = 1, expand=True)
    restorderitem_orderable_df['order_date'] = data_columns[0]
    restorderitem_orderable_df['order_time'] = data_columns[1]

    # Drop some unnecessery columns for light using
    final_df = restorderitem_orderable_df.drop(columns=['creation_date','restaurant_id','orderable_id'])

    # Creating view for best_seller_product per restaurant
    best_seller_df = final_df.groupby(['name','product_name'])["amount"].sum().sort_values(ascending=False).reset_index()

    ### Filtering for restaurant_name
    result_df = best_seller_df[best_seller_df['name'] == restaurant_name]  ## -> restaurant_name comes from select_box

    ### Create figure
    fig = px.scatter(result_df, x='product_name', y='amount', color='amount', size='amount', title=f'{restaurant_name} Best Seller Products (All Time)')
    fig.update_xaxes(title='Product', showticklabels=False)
    fig.update_yaxes(title='Amount(Pcs)', showticklabels=True)
    fig.update_layout(
        title_font_family='Times New Roman',
        title_font_color='darkolivegreen',
        font_family='Roboto Mono',
        font_color='darksalmon',
    )

    return fig

def get_loyality_fig(restaurant_name:str) -> px.bar:
    restaurant_df.rename(columns={"id":"restaurant_id"},inplace=True)
    orderables_df.rename(columns={"id":"orderable_id"},inplace=True)
    orderables_df.rename(columns={"name":"product_name"},inplace=True)

    # Merging dataframes
    rest_order_df = pd.merge(restaurant_df[['name','restaurant_id','city']], order_df, how="inner", on="restaurant_id")
    rest_order_df.rename(columns={"id":"order_id"},inplace=True)
    restorder_item_df = pd.merge(rest_order_df, orderItem_df[['order_id', 'amount', 'orderable_id']], how='inner', on='order_id')
    restorderitem_orderable_df = pd.merge(restorder_item_df,orderables_df[['price','orderable_id','product_name',]], how='inner', on='orderable_id')

    # Split creation_date as order date and order time
    data_columns = restorderitem_orderable_df['creation_date'].str.split(" ", n = 1, expand=True)
    restorderitem_orderable_df['order_date'] = data_columns[0]
    restorderitem_orderable_df['order_time'] = data_columns[1]

    # Drop some unnecessery columns for light using
    final_df = restorderitem_orderable_df.drop(columns=['creation_date','restaurant_id','orderable_id'])

    loyality_count = final_df[final_df['name'] == 'Brooklyn Democratic Club']['customer_id'].nunique() * 0.1
    data = final_df[final_df['name'] == restaurant_name].groupby(['customer_id'])['order_id'].count().sort_values(ascending=False).head(int(loyality_count)).reset_index()
    data['customer_id'] = data['customer_id'].astype(str)

    fig = px.bar(
    data, x='order_id', y="customer_id", orientation='h', color='order_id', 
    color_continuous_scale=px.colors.sequential.haline,
    title=f'{restaurant_name} - Loyality Programme (%10)'
    )
    fig.update_layout(
        title_font_family='Times New Roman',
        title_font_color='darkolivegreen',
        font_family='Roboto Mono',
        font_color='darksalmon',
    )
    fig.update_xaxes(title='Order Count', showticklabels=True)
    fig.update_yaxes(title='Product ID', showticklabels=True, autorange="reversed")
    
    return fig

option = st.selectbox(
    'Restaurant',
    ('Brooklyn Democratic Club', 'Harrys Bar', 'Sheraton Blackstone Chicago')
)

st.plotly_chart(get_bestseller_fig(option), use_container_width=True)
st.plotly_chart(get_loyality_fig(option), use_container_width=True)