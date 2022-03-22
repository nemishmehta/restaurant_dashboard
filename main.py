import pandas as pd
import plotly.express as px
import streamlit as st


def global_insights(df):

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


def fav_dish(fav_dish_df, by_type, city):

    fav_dish_city = fav_dish_df.loc[(fav_dish_df["city"] == city) & (
        fav_dish_df[by_type] == fav_dish_df.loc[
            fav_dish_df["city"] == city][by_type].max()), "dish_name"].iloc[0]

    return fav_dish_city


def fav_rest(fav_rest_df, by_type, city):

    fav_rest_city = fav_rest_df.loc[(fav_rest_df["city"] == city) & (
        fav_rest_df[by_type] == fav_rest_df.loc[
            fav_rest_df["city"] == city][by_type].max()), "rest_name"].iloc[0]

    return fav_rest_city


def plot_order_data(fav_dish_df, fav_dish_city_ny, fav_dish_city_sf, by_type):
    col1, col2 = st.columns(2)
    col1.metric(
        label='New York',
        value=fav_dish_city_ny,
        delta='{:,} orders'.format(
            fav_dish_df[fav_dish_df["city"] == "New York"][by_type].max()))
    col2.metric(label='San Francisco',
                value=fav_dish_city_sf,
                delta='{:,} orders'.format(fav_dish_df[
                    fav_dish_df["city"] == "San Francisco"][by_type].max()))


def plot_revenue_data(fav_dish_df, fav_dish_city_ny, fav_dish_city_sf,
                      by_type):
    col1, col2 = st.columns(2)
    col1.metric(
        label='New York',
        value=fav_dish_city_ny,
        delta='${:,}'.format(
            fav_dish_df[fav_dish_df["city"] == "New York"][by_type].max()))
    col2.metric(label='San Francisco',
                value=fav_dish_city_sf,
                delta='${:,}'.format(fav_dish_df[
                    fav_dish_df["city"] == "San Francisco"][by_type].max()))


def allergy_info(cust_db, allergies):

    allergies_count = []

    for allergy in allergies:
        allergies_count.append(cust_db[allergy].sum())

    allergy_df = pd.DataFrame({
        "Allergies": allergies,
        "Number of People Suffering": allergies_count
    })

    allergy_df = allergy_df.sort_values(by=['Number of People Suffering'])

    fig = px.bar(allergy_df, x="Allergies", y="Number of People Suffering")
    fig.update_traces(marker_color='RoyalBlue')
    st.plotly_chart(fig, use_container_width=True)


def allergy_food_orders(df, allergy_choice):

    # Top 5 dishes ordered by a person with chosen allergy
    top_5_dishes_ord = df[df[allergy_choice] == 1.0].groupby(
        'dish_name')['amount'].sum().sort_values(
            ascending=False).head(5).reset_index()

    # Plot graph
    fig = px.bar(top_5_dishes_ord, x="dish_name", y="amount")
    fig.update_traces(marker_color='RoyalBlue')
    st.plotly_chart(fig, use_container_width=True)


def allergy_food_revenue(df, allergy_choice):

    # Top 5 dishes ordered by a person with chosen allergy
    top_5_dishes_rev = df[df[allergy_choice] == 1.0].groupby(
        'dish_name')['revenue'].sum().sort_values(
            ascending=False).head(5).reset_index()

    # Plot graph
    fig = px.bar(top_5_dishes_rev, x="dish_name", y="revenue")
    fig.update_traces(marker_color='RoyalBlue')
    st.plotly_chart(fig, use_container_width=True)


def allergy_rest_revenue(df, allergy_choice):
    # Top 5 restaurants ordered by a person with chosen allergy
    top_5_dishes_rev = df[df[allergy_choice] == 1.0].groupby(
        'rest_name')['revenue'].sum().sort_values(
            ascending=False).head(5).reset_index()

    # Plot graph
    fig = px.bar(top_5_dishes_rev, x="rest_name", y="revenue")
    fig.update_traces(marker_color='RoyalBlue')
    st.plotly_chart(fig, use_container_width=True)


def rest_revenue_from_allergy(df, allergy_choice, rest_choice):
    all_rest_allergy = df[df[allergy_choice] == 1.0].groupby(
        'rest_name')['revenue'].sum().sort_values(
            ascending=False).reset_index()
    rest_rev_allergy = all_rest_allergy[all_rest_allergy['rest_name'] ==
                                        rest_choice]

    st.write(rest_rev_allergy)


def main():
    if __name__ == '__main__':
        df = pd.read_csv('data/full_table.csv', index_col=0)

        st.title("Restaurant Dashboard")

        st.subheader("Global Insights")
        global_insights(df)

        # Favourite dish
        st.write("#")
        st.markdown('### Most Popular Dish')

        # No. of orders
        st.markdown('**Number of orders**')
        fav_dish_df_ord = df.groupby(['city', 'dish_name'],
                                     as_index=False)["amount"].sum()
        fav_dish_city_ny_ord = fav_dish(fav_dish_df_ord, "amount", "New York")
        fav_dish_city_sf_ord = fav_dish(fav_dish_df_ord, "amount",
                                        "San Francisco")
        plot_order_data(fav_dish_df_ord, fav_dish_city_ny_ord,
                        fav_dish_city_sf_ord, "amount")

        # Revenue
        st.markdown('**Revenue**')
        fav_dish_df_rev = df.groupby(['city', 'dish_name'],
                                     as_index=False)["revenue"].sum()
        fav_dish_city_ny_rev = fav_dish(fav_dish_df_rev, "revenue", "New York")
        fav_dish_city_sf_rev = fav_dish(fav_dish_df_rev, "revenue",
                                        "San Francisco")
        plot_revenue_data(fav_dish_df_rev, fav_dish_city_ny_rev,
                          fav_dish_city_sf_rev, "revenue")

        # Favourite restaurant
        st.write("#")
        st.markdown('### Most Popular Restaurant')

        # No. of orders
        st.markdown('**Number of orders**')
        fav_rest_df_ord = df.groupby(['city', 'rest_name'],
                                     as_index=False)["amount"].sum()
        fav_rest_city_ny_ord = fav_rest(fav_rest_df_ord, "amount", "New York")
        fav_rest_city_sf_ord = fav_rest(fav_rest_df_ord, "amount",
                                        "San Francisco")
        plot_order_data(fav_rest_df_ord, fav_rest_city_ny_ord,
                        fav_rest_city_sf_ord, "amount")

        # Revenue
        st.markdown('**Revenue**')
        fav_rest_df_rev = df.groupby(['city', 'rest_name'],
                                     as_index=False)["revenue"].sum()
        fav_rest_city_ny_rev = fav_rest(fav_rest_df_rev, "revenue", "New York")
        fav_rest_city_sf_rev = fav_rest(fav_rest_df_rev, "revenue",
                                        "San Francisco")
        plot_revenue_data(fav_rest_df_rev, fav_rest_city_ny_rev,
                          fav_rest_city_sf_rev, "revenue")

        # Allergy Information
        st.write('#')
        st.markdown('### Allergies')
        st.write('Allergies v/s Number of People Suffering')
        cust_db = pd.read_csv('data/complete_customer_database.csv',
                              index_col=0)

        # Create a list of all allergies
        allergies = cust_db.drop(['customer_id'], axis=1).columns.tolist()

        allergy_info(cust_db, allergies)

        # Allergy Food Ordering
        st.write('#')

        # Dropdown for user to choose allergy
        allergy_choice = st.selectbox(label='Choose an allergy',
                                      options=allergies)
        st.markdown('#### Top 5 Dishes Ordered by Allergy')
        st.write("Dishes v/s Amount of Times Ordered")
        allergy_food_orders(df, allergy_choice)
        st.write("###")
        st.write("Dishes v/s Revenue Generated")
        allergy_food_revenue(df, allergy_choice)
        st.write("###")

        st.markdown('#### Top 5 Restaurants Based on Allergy')
        st.write("Restaurants v/s Revenue Generated")
        allergy_rest_revenue(df, allergy_choice)

        df_rest = pd.read_csv('data/ODL_RESTAURANT.csv', usecols=['name'])
        df_rest.loc[len(df_rest.index)] = '(All)'
        df_rest = df_rest.sort_values(by=['name'], ignore_index=True)

        rest_choice = st.selectbox(label='Choose a restaurant',
                                   options=df_rest)

        rest_revenue_from_allergy(df, allergy_choice, rest_choice)
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
