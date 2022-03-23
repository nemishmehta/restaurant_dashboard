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

    fig = px.bar(allergy_df,
                 x="Allergies",
                 y="Number of People Suffering",
                 color="Number of People Suffering")
    st.plotly_chart(fig, use_container_width=True)


def allergy_food_orders(df, allergy_choice, by_choice_allergy):

    # Top 5 dishes ordered by a person with chosen allergy
    top_5_dishes_ord = df[df[allergy_choice] == 1.0].groupby(
        'dish_name')[by_choice_allergy].sum().sort_values(
            ascending=False).head(5).reset_index()

    # Plot graph
    fig = px.bar(top_5_dishes_ord,
                 x="dish_name",
                 y=by_choice_allergy,
                 color=by_choice_allergy)
    st.plotly_chart(fig, use_container_width=True)


def allergy_rest_revenue(df, allergy_choice, by_choice_allergy):
    # Top 5 restaurants ordered by a person with chosen allergy
    top_5_dishes_rev = df[df[allergy_choice] == 1.0].groupby(
        'rest_name')[by_choice_allergy].sum().sort_values(
            ascending=False).head(5).reset_index()

    # Plot graph
    fig = px.bar(top_5_dishes_rev,
                 x="rest_name",
                 y=by_choice_allergy,
                 color=by_choice_allergy)
    st.plotly_chart(fig, use_container_width=True)


def rest_revenue_from_allergy(df, allergy_choice, rest_choice):
    all_rest_allergy = df[df[allergy_choice] == 1.0].groupby(
        'rest_name')['revenue'].sum().sort_values(
            ascending=False).reset_index()
    rest_rev_allergy = all_rest_allergy[all_rest_allergy['rest_name'] ==
                                        rest_choice]

    st.write(rest_rev_allergy)


def trends(df, rest_choice, category, by_type):
    if rest_choice == '(All)':
        # Plot graph
        total_rev = df.groupby(category)[by_type].sum().sort_values(
            ascending=False).reset_index()
        fig = px.bar(total_rev, x=category, y=by_type, color=by_type)
        st.plotly_chart(fig, use_container_width=True)
    else:
        total_rev = df.groupby([
            'rest_name', category
        ])[by_type].sum().sort_values(ascending=False).reset_index()
        rest_rev = total_rev[total_rev['rest_name'] == rest_choice]
        fig = px.bar(rest_rev, x=category, y=by_type, color=by_type)
        st.plotly_chart(fig, use_container_width=True)


def rest_vs_all(df, rest_choice, by_type):

    if rest_choice == '(All)':
        st.markdown("##### Total {}: {:,}".format(by_type,
                                                  df[by_type].sum().round(0)))
        st.markdown(
            "##### Total {} v/s Total {} by all restaurants: {}%".format(
                by_type, by_type,
                (df[by_type].sum() / df[by_type].sum()) * 100))
    else:
        st.markdown("##### Total {}: {:,}".format(
            by_type,
            df[df['rest_name'] == rest_choice][by_type].sum().round(0)))
        st.markdown(
            "##### Total {} v/s Total {} by all restaurants: {}%".format(
                by_type, by_type,
                ((df[df['rest_name'] == rest_choice][by_type].sum() /
                  df[by_type].sum()) * 100).round(2)))


def loyalty_prog_ord(df, rest_choice):
    if rest_choice == '(All)':
        loyality_count = df['customer_id'].value_counts().rename_axis(
            'customer_id').reset_index(name='amount')
        loyality_count = loyality_count.head(int(len(loyality_count) * 0.01))
        loyality_count['customer_id'] = loyality_count['customer_id'].astype(
            str)
        fig = px.bar(loyality_count,
                     x='amount',
                     y='customer_id',
                     orientation='h',
                     color='amount')
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(fig, use_container_width=True)
    else:
        loyality_count = df.groupby([
            'rest_name', 'customer_id'
        ])['amount'].sum().sort_values(ascending=False).reset_index()
        loyality_cust = loyality_count[loyality_count['rest_name'] ==
                                       rest_choice]
        loyality_cust = loyality_cust.head(int(len(loyality_cust) * 0.01))
        loyality_cust['customer_id'] = loyality_cust['customer_id'].astype(str)
        fig = px.bar(loyality_cust,
                     x='amount',
                     y='customer_id',
                     orientation='h',
                     color='amount')
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(fig, use_container_width=True)


def disc_prog_ord(df, rest_choice):
    if rest_choice == '(All)':
        disc_count = df['customer_id'].value_counts().rename_axis(
            'customer_id').reset_index(name='amount')
        disc_count = disc_count.tail(int(len(disc_count) * 0.01))
        disc_count['customer_id'] = disc_count['customer_id'].astype(str)
        fig = px.bar(disc_count,
                     x='amount',
                     y='customer_id',
                     orientation='h',
                     color='amount')
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(fig, use_container_width=True)
    else:
        disc_count = df.groupby([
            'rest_name', 'customer_id'
        ])['amount'].sum().sort_values(ascending=False).reset_index()
        disc_cust = disc_count[disc_count['rest_name'] == rest_choice]
        disc_cust = disc_cust.tail(int(len(disc_cust) * 0.01))
        disc_cust['customer_id'] = disc_cust['customer_id'].astype(str)
        fig = px.bar(disc_cust,
                     x='amount',
                     y='customer_id',
                     orientation='h',
                     color='amount')
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(fig, use_container_width=True)


def loyalty_prog_rev(df, rest_choice):
    if rest_choice == '(All)':
        loyality_count = df.groupby('customer_id')['revenue'].sum(
        ).sort_values(ascending=False).reset_index()
        loyality_count = loyality_count.head(int(len(loyality_count) * 0.01))
        loyality_count['customer_id'] = loyality_count['customer_id'].astype(
            str)
        fig = px.bar(loyality_count,
                     x='revenue',
                     y='customer_id',
                     orientation='h',
                     color='revenue')
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(fig, use_container_width=True)
    else:
        loyality_count = df.groupby([
            'rest_name', 'customer_id'
        ])['revenue'].sum().sort_values(ascending=False).reset_index()
        loyality_cust = loyality_count[loyality_count['rest_name'] ==
                                       rest_choice]
        loyality_cust = loyality_cust.head(int(len(loyality_cust) * 0.01))
        loyality_cust['customer_id'] = loyality_cust['customer_id'].astype(str)
        fig = px.bar(loyality_cust,
                     x='revenue',
                     y='customer_id',
                     orientation='h',
                     color='revenue')
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(fig, use_container_width=True)


def disc_prog_rev(df, rest_choice):
    if rest_choice == '(All)':
        disc_count = df.groupby('customer_id')['revenue'].sum().sort_values(
            ascending=False).reset_index()
        disc_count = disc_count.tail(int(len(disc_count) * 0.01))
        disc_count['customer_id'] = disc_count['customer_id'].astype(str)
        fig = px.bar(disc_count,
                     x='revenue',
                     y='customer_id',
                     orientation='h',
                     color='revenue')
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(fig, use_container_width=True)
    else:
        disc_count = df.groupby([
            'rest_name', 'customer_id'
        ])['revenue'].sum().sort_values(ascending=False).reset_index()
        disc_cust = disc_count[disc_count['rest_name'] == rest_choice]
        disc_cust = disc_cust.tail(int(len(disc_cust) * 0.01))
        disc_cust['customer_id'] = disc_cust['customer_id'].astype(str)
        fig = px.bar(disc_cust,
                     x='revenue',
                     y='customer_id',
                     orientation='h',
                     color='revenue')
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(fig, use_container_width=True)


def best_seller(df, rest_choice, by_type):
    if rest_choice == '(All)':
        st.markdown("##### Top 10% Best Selling Dishes")
        best_seller_df = df.groupby('dish_name')[by_type].sum().sort_values(
            ascending=False).reset_index()
        best_seller_df = best_seller_df.head(int(len(best_seller_df) * 0.01))
        fig = px.bar(best_seller_df, x='dish_name', y=by_type, color=by_type)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.markdown("##### Best Selling Dishes")
        best_seller_df = df.groupby([
            'rest_name', 'dish_name'
        ])[by_type].sum().sort_values(ascending=False).reset_index()
        best_seller_rest = best_seller_df[best_seller_df['rest_name'] ==
                                          rest_choice]
        fig = px.bar(best_seller_rest, x='dish_name', y=by_type, color=by_type)
        st.plotly_chart(fig, use_container_width=True)


def least_seller(df, rest_choice, by_type):
    if rest_choice == '(All)':
        st.markdown("##### Top 10% Least Selling Dishes")
        least_seller_df = df.groupby('dish_name')[by_type].sum().sort_values(
            ascending=True).reset_index()
        least_seller_df = least_seller_df.head(int(
            len(least_seller_df) * 0.01))
        fig = px.bar(least_seller_df, x='dish_name', y=by_type, color=by_type)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.markdown("##### Least Selling Dishes")
        least_seller_df = df.groupby([
            'rest_name', 'dish_name'
        ])[by_type].sum().sort_values(ascending=True).reset_index()
        least_seller_rest = least_seller_df[least_seller_df['rest_name'] ==
                                            rest_choice]
        fig = px.bar(least_seller_rest,
                     x='dish_name',
                     y=by_type,
                     color=by_type)
        st.plotly_chart(fig, use_container_width=True)


def main():
    if __name__ == '__main__':
        df = pd.read_csv('data/full_table.csv', index_col=0)

        st.title("Food Delivery Dashboard")

        st.subheader("Global Insights")
        global_insights(df)

        # Favourite dish
        st.write("#")
        st.markdown('#### Most Popular Dish')

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
        st.markdown('#### Most Popular Restaurant')

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

        df_rest = pd.read_csv('data/ODL_RESTAURANT.csv', usecols=['name'])
        df_rest.loc[len(df_rest.index)] = '(All)'
        df_rest = df_rest.sort_values(by=['name'], ignore_index=True)

        st.write("#")
        st.markdown("### Deep Dive")
        rest_choice = st.selectbox(label='Choose a restaurant',
                                   options=df_rest)
        by_type_choice = st.selectbox(label='Select type',
                                      options=("amount", "revenue"),
                                      key=1)

        st.write("#")
        st.markdown("#### Restaurant Overview")
        rest_vs_all(df, rest_choice, by_type_choice)

        # Revenue Maximization
        st.write("#")
        st.subheader("Revenue Maximization")
        st.markdown(
            f"##### Loyalty Programs to Top 1% Customers by {by_type_choice}")
        if by_type_choice == 'amount':
            loyalty_prog_ord(df, rest_choice)
        else:
            loyalty_prog_rev(df, rest_choice)

        st.markdown(
            f"##### Discount Offers to Bottom 1% Customers by {by_type_choice}"
        )
        if by_type_choice == 'amount':
            disc_prog_ord(df, rest_choice)
        else:
            disc_prog_rev(df, rest_choice)

        #st.write("INSERT GRAPH FOR CUSTOMER ORDERING PATTERNS")

        #st.write("INSERT GRAPH FOR COMPETITOR RESTAURANTS")

        # Cost Optimization
        st.subheader("Cost Optimization")

        st.write("##### Restaurant v/s Period of Day")
        trends(df, rest_choice, "period", by_type_choice)

        st.write("##### Restaurant v/s Day of the Week")
        trends(df, rest_choice, "order_day", by_type_choice)

        st.write("##### Restaurant v/s Season")
        trends(df, rest_choice, "order_season", by_type_choice)

        best_seller(df, rest_choice, by_type_choice)

        least_seller(df, rest_choice, by_type_choice)

        # st.write(
        #     "INSERT GRAPH FOR IMPACT ON REVENUE IF LEAST SELLING DISHES ARE DISCARDED"
        # )
        # Allergy Information
        st.write('#')
        st.markdown('### Allergies')
        st.write('##### Allergies v/s Number of People Suffering')
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
        by_type_choice_allergy = st.selectbox(label='Select type',
                                              options=("amount", "revenue"),
                                              key=2)
        st.markdown('#### Top 5 Dishes Ordered by Allergy')
        st.write(f"##### Dishes v/s {by_type_choice_allergy}")
        allergy_food_orders(df, allergy_choice, by_type_choice_allergy)

        st.markdown('#### Top 5 Restaurants Based on Allergy')
        st.write(f"##### Restaurants v/s {by_type_choice_allergy}")
        allergy_rest_revenue(df, allergy_choice, by_type_choice_allergy)

        #rest_revenue_from_allergy(df, allergy_choice, rest_choice)


main()
