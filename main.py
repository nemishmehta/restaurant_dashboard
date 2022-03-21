import pandas as pd
import streamlit as st


def general_insights(df):

    # Unique Customers
    df_unique_cust = df.drop_duplicates(subset=['customer_id'])
    df_unique_cust.groupby('city')['customer_id'].nunique()

    # New York
    st.markdown('**New York**')
    col1, col2, col3 = st.columns(3)
    col1.metric(label='Aggregate Orders',
                value="{:,}".format(
                    df.groupby('city')['order_id'].nunique()['New York']))
    col2.metric(label='Unique Customers',
                value="{:,}".format(
                    df_unique_cust.groupby('city')['customer_id'].nunique()
                    ['New York']))
    col3.metric(label='Total Revenue',
                value="${:,}".format(
                    df.groupby('city')['revenue'].sum()['New York'].round(0)))

    # San Francisco
    st.markdown('**San Francisco**')
    col1, col2, col3 = st.columns(3)
    col1.metric(label='Aggregate Orders',
                value="{:,}".format(
                    df.groupby('city')['order_id'].nunique()['San Francisco']))
    col2.metric(label='Unique Customers',
                value="{:,}".format(
                    df_unique_cust.groupby('city')['customer_id'].nunique()
                    ['San Francisco']))
    col3.metric(
        label='Total Revenue',
        value="${:,}".format(
            df.groupby('city')['revenue'].sum()['San Francisco'].round(0)))


def fav_dish_orders(df):

    fav_dish_orders_df = df.groupby(['city', 'dish_name'],
                                    as_index=False)['amount'].sum()

    ny_fav_dish_orders = fav_dish_orders_df.loc[
        (fav_dish_orders_df["city"] == "New York") &
        (fav_dish_orders_df['amount'] == fav_dish_orders_df.loc[
            fav_dish_orders_df["city"] == "New York"]['amount'].max()),
        "dish_name"].iloc[0]

    sf_fav_dish_orders = fav_dish_orders_df.loc[
        (fav_dish_orders_df["city"] == "San Francisco") &
        (fav_dish_orders_df['amount'] == fav_dish_orders_df.loc[
            fav_dish_orders_df["city"] == "San Francisco"]['amount'].max()),
        "dish_name"].iloc[0]

    # No. of orders
    st.markdown('**Number of orders**')

    col1, col2 = st.columns(2)
    col1.metric(label='New York',
                value=ny_fav_dish_orders,
                delta='{:,} orders'.format(fav_dish_orders_df[
                    fav_dish_orders_df["city"] == "New York"]["amount"].max()))
    col2.metric(label='San Francisco',
                value=sf_fav_dish_orders,
                delta='{:,} orders'.format(
                    fav_dish_orders_df[fav_dish_orders_df["city"] ==
                                       "San Francisco"]["amount"].max()))


def fav_dish_revenue(df):

    fav_dish_revenue_df = df.groupby(['city', 'dish_name'],
                                     as_index=False)['revenue'].sum()

    ny_fav_dish_revenue = fav_dish_revenue_df.loc[
        (fav_dish_revenue_df["city"] == "New York") &
        (fav_dish_revenue_df['revenue'] == fav_dish_revenue_df.loc[
            fav_dish_revenue_df["city"] == "New York"]['revenue'].max()),
        "dish_name"].iloc[0]

    sf_fav_dish_revenue = fav_dish_revenue_df.loc[
        (fav_dish_revenue_df["city"] == "San Francisco") &
        (fav_dish_revenue_df['revenue'] == fav_dish_revenue_df.loc[
            fav_dish_revenue_df["city"] == "San Francisco"]['revenue'].max()),
        "dish_name"].iloc[0]

    col1, col2 = st.columns(2)
    col1.metric(label='New York',
                value=ny_fav_dish_revenue,
                delta='${:,}'.format(
                    fav_dish_revenue_df[fav_dish_revenue_df["city"] ==
                                        "New York"]["revenue"].max()))
    col2.metric(label='San Francisco',
                value=sf_fav_dish_revenue,
                delta='${:,}'.format(
                    fav_dish_revenue_df[fav_dish_revenue_df["city"] ==
                                        "San Francisco"]["revenue"].max()))


def fav_rest_orders(df):

    fav_rest_orders_df = df.groupby(['city', 'rest_name'],
                                    as_index=False)['amount'].sum()

    ny_fav_rest_orders = fav_rest_orders_df.loc[
        (fav_rest_orders_df["city"] == "New York") &
        (fav_rest_orders_df['amount'] == fav_rest_orders_df.loc[
            fav_rest_orders_df["city"] == "New York"]['amount'].max()),
        "rest_name"].iloc[0]

    sf_fav_rest_orders = fav_rest_orders_df.loc[
        (fav_rest_orders_df["city"] == "San Francisco") &
        (fav_rest_orders_df['amount'] == fav_rest_orders_df.loc[
            fav_rest_orders_df["city"] == "San Francisco"]['amount'].max()),
        "rest_name"].iloc[0]

    # No. of orders
    st.markdown('**Number of orders**')

    col1, col2 = st.columns(2)
    col1.metric(label='New York',
                value=ny_fav_rest_orders,
                delta='{:,} orders'.format(fav_rest_orders_df[
                    fav_rest_orders_df["city"] == "New York"]["amount"].max()))
    col2.metric(label='San Francisco',
                value=sf_fav_rest_orders,
                delta='{:,} orders'.format(
                    fav_rest_orders_df[fav_rest_orders_df["city"] ==
                                       "San Francisco"]["amount"].max()))


def fav_rest_revenue(df):

    fav_rest_revenue_df = df.groupby(['city', 'rest_name'],
                                     as_index=False)['revenue'].sum()

    ny_fav_rest_revenue = fav_rest_revenue_df.loc[
        (fav_rest_revenue_df["city"] == "New York") &
        (fav_rest_revenue_df['revenue'] == fav_rest_revenue_df.loc[
            fav_rest_revenue_df["city"] == "New York"]['revenue'].max()),
        "rest_name"].iloc[0]

    sf_fav_rest_revenue = fav_rest_revenue_df.loc[
        (fav_rest_revenue_df["city"] == "San Francisco") &
        (fav_rest_revenue_df['revenue'] == fav_rest_revenue_df.loc[
            fav_rest_revenue_df["city"] == "San Francisco"]['revenue'].max()),
        "rest_name"].iloc[0]

    # By revenue
    st.markdown('**Revenue**')

    col1, col2 = st.columns(2)
    col1.metric(label='New York',
                value=ny_fav_rest_revenue,
                delta='${:,}'.format(
                    fav_rest_revenue_df[fav_rest_revenue_df["city"] ==
                                        "New York"]["revenue"].max()))
    col2.metric(label='San Francisco',
                value=sf_fav_rest_revenue,
                delta='${:,}'.format(
                    fav_rest_revenue_df[fav_rest_revenue_df["city"] ==
                                        "San Francisco"]["revenue"].max()))


# Code Refactoring - TBD
def fav_dish(df, by_type, city):

    fav_dish_df = df.groupby(['city', 'dish_name'],
                             as_index=False)[by_type].sum()

    fav_dish_city = fav_dish_df.loc[(fav_dish_df["city"] == city) & (
        fav_dish_df[by_type] == fav_dish_df.loc[
            fav_dish_df["city"] == city][by_type].max()), "dish_name"].iloc[0]


def main():
    if __name__ == '__main__':
        df = pd.read_csv('data/full_table_v0.4.csv', index_col=0)

        st.title("Restaurant Dashboard")

        st.subheader("General Insights")
        general_insights(df)

        # Favourite dish
        st.markdown('**Favourite Dish**')
        fav_dish_orders(df)
        fav_dish_revenue(df)
        #fav_dish(df, "amount", "New York")

        # Favourite restaurant
        st.markdown('**Favourite Restaurant**')
        fav_rest_orders(df)
        fav_rest_revenue(df)

        df_rest = pd.read_csv('data/ODL_RESTAURANT.csv', usecols=['name'])
        df_rest.loc[len(df_rest.index)] = '(All)'
        df_rest = df_rest.sort_values(by=['name'], ignore_index=True)

        rest_choice = st.selectbox(label='Choose a restaurant',
                                   options=df_rest)

        st.write(rest_choice)

        # Revenue Maximization
        st.subheader("Revenue Maximization")

        st.write("INSERT GRAPH FOR TOTAL REVENUE GENERATED")

        st.write("INSERT GRAPH FOR AVG. REVENUE/ORDER")

        st.write(
            "INSERT GRAPH FOR MOST FREQUENT CUSTOMERS --> LOYALTY PROGRAM")

        st.write("INSERT GRAPH FOR LEAST FREQUENT CUSTOMERS --> DISCOUNTS")

        st.write("INSERT GRAPH FOR CUSTOMER ORDERING PATTERNS")

        st.write("INSERT GRAPH FOR COMPETITOR RESTAURANTS")

        # Cost Optimization
        st.subheader("Cost Optimization")

        st.write("INSERT GRAPH FOR ORDER TIMING TRENDS")

        st.write("INSERT GRAPH FOR ORDER DAY TRENDS")

        st.write("INSERT GRAPH FOR ORDER SEASONAL TRENDS")

        st.write("INSERT GRAPH FOR BEST SELLING DISHES")

        st.write("INSERT GRAPH FOR LEAST SELLING DISHES")

        st.write(
            "INSERT GRAPH FOR IMPACT ON REVENUE IF LEAST SELLING DISHES ARE DISCARDED"
        )


main()
