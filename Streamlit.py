import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import seaborn as sns


# in the dropdown (with no options)
def general_time_trend(unstacked_gtb):
    # "start" and "end" as parameters
    # df = unstacked_gtb[(pd.to_datetime(unstacked_gtb["order_creation_date"]) > start)
    # & (pd.to_datetime(unstacked_gtb["order_creation_date"]) < end)]
    # returned "Invalid comparison between dtype=datetime64[ns] and date"
    # I don't know which one is which
    df = unstacked_gtb
    fig = plt.figure(figsize=(12, 8), dpi=100)
    sns.barplot(data=df, x="order_creation_date", y="order_id")
    plt.title("General Orders Trend Through Time")
    plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    plt.xlabel("Time")
    plt.ylabel("Amount of Orders")
    st.pyplot(fig)


# in the dropdown (with no options)
def general_revenue_trend(unstacked_grb):
    fig = plt.figure(figsize=(12, 8), dpi=100)
    sns.barplot(data=unstacked_grb, x="order_creation_date", y="revenue")
    plt.title("General Revenue Trend Through Time")
    plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    plt.xlabel("Time")
    plt.ylabel("Revenue")
    st.pyplot(fig)


# Not in the dropdown
# No real added value as is in my opinion
def orders_per_day_heatmap(orders_per_day):
    fig = plt.figure(figsize=(12, 8), dpi=100)
    sns.heatmap(orders_per_day, annot=orders_per_day, fmt="g")
    st.pyplot(fig)


# in the dropdown (with no options)
def orders_per_day_barchart(orders_per_day):
    df = orders_per_day.reset_index()
    chart = alt.Chart(df)
    c = chart.mark_bar().encode(x="index", y="order_day")
    st.altair_chart(c, use_container_width=True)


# in the dropdown (with no options)
def day_time_heatmap_trends(unstacked_dt_trend):
    df = unstacked_dt_trend
    fig = plt.figure(figsize=(12, 8), dpi=100)
    sns.heatmap(df, annot=df, fmt="g", linewidth=1, cmap="Blues")
    st.pyplot(fig)


# Not in the dropdown
# Could have added value if I could implement the "hue" option
def day_time_barchart_trends(unstacked_dt_trend):
    fig = plt.figure(figsize=(12, 8), dpi=100)
    ticks = [0, 1, 2, 3, 4, 5, 6]
    labels = ["Friday", "Monday", "Saturday", "Sunday", "Thursday", "Tuesday", "Wednesday"]
    sns.barplot(data=unstacked_dt_trend)
    plt.xticks(ticks=ticks, labels=labels)
    plt.xticks(rotation=90)
    st.pyplot(fig)


# in the dropdown (with no options)
def day_time_revenue_heatmap(unstacked_dt_revenue):
    fig = plt.figure(figsize=(12, 8), dpi=100)
    sns.heatmap(unstacked_dt_revenue, annot=unstacked_dt_revenue, fmt="g", linewidth=1, cmap="Blues")
    st.pyplot(fig)


# Not in the dropdown
# Could have added value if I could implement the "hue" option
def day_time_revenue_barchart(unstacked_dt_revenue):
    fig = plt.figure(figsize=(12, 8), dpi=100)
    ticks = [0, 1, 2, 3, 4, 5, 6]
    labels = ["Friday", "Monday", "Saturday", "Sunday", "Thursday", "Tuesday", "Wednesday"]
    sns.barplot(data=unstacked_dt_revenue)
    plt.xticks(ticks=ticks, labels=labels)
    plt.xticks(rotation=90)
    plt.ticklabel_format(style='plain', axis='y')


# In the dropdown (with no options)
# Could it be interesting if selecting Restaurant? Dish? Something else?
def seasons_trends_barchart(unstacked_seasons_trend):
    fig = plt.figure(figsize=(12, 8), dpi=100)
    sns.barplot(
        data=unstacked_seasons_trend,
        x=unstacked_seasons_trend["order_season"],
        y=unstacked_seasons_trend["order_id"]
    )
    st.pyplot(fig)


# In the dropdown (with no options)
# Could it be interesting if selecting Restaurant? Dish? Something else?
def seasons_revenue(unstacked_revenue_per_season):
    df = unstacked_revenue_per_season
    fig = plt.figure(figsize=(12, 8), dpi=100)
    sns.barplot(data=df, x=df["order_season"], y=df["revenue"])
    st.pyplot(fig)


# This is a DF that was updated with the new columns here
# Mine was located in same folder
data = pd.read_csv("full_table_v0.4.csv", index_col=0)

# All the subsets DF generated from data above
# Same name as function arguments but in ALL CAPS to make it easier
# Some were not used finally, could be useful to sort it out later
GENERAL_TIME_BARS = pd.DataFrame(data.groupby(["order_creation_date"])["order_id"].count())
UNSTACKED_GTB = GENERAL_TIME_BARS.reset_index()
GENERAL_REVENUE_BARS = pd.DataFrame(data.groupby(["order_creation_date"])["revenue"].sum())
UNSTACKED_GRB = GENERAL_REVENUE_BARS.reset_index()
ORDERS_PER_DAY = pd.DataFrame(data["order_day"].value_counts(ascending=False))
DAY_TIME_TREND = pd.DataFrame(data.groupby(["period", "order_day"])["order_id"].count())
UNSTACKED_DT_TREND = DAY_TIME_TREND.unstack()
DAY_TIME_REVENUE = pd.DataFrame(data.groupby(["period", "order_day"])["revenue"].sum())
UNSTACKED_DT_REVENUE = DAY_TIME_REVENUE.unstack()
SEASONS_TREND = pd.DataFrame(data.groupby(["order_season"])["order_id"].count())
UNSTACKED_SEASONS_TREND = SEASONS_TREND.reset_index()
REVENUE_PER_SEASON = pd.DataFrame(data.groupby(["order_season"])["revenue"].sum())
UNSTACKED_REVENUE_PER_SEASON = REVENUE_PER_SEASON.reset_index()


header = st.container()


# This is the beginning of the "main". Must be indented inside the container object
# Allows to divide the page in multiple containers and include columns (not interesting considering the lack of time)

with header:
    st.title("Bullshit Inc. Delivery")
    st.text("The Data Analysis")

    trends_tickers = [
        "General Orders Trend",
        "General Revenue Trend",
        "Day / Period Heatmap Trend",
        "Day / Period Revenue Trend",
        "Orders Per Day Barchart",
        "Seasonal Trends Barchart",
        "Seasonal Revenue Trends"
    ]
    trends = st.multiselect(label="Select What to plot", options=trends_tickers)

    if "General Orders Trend" in trends:
        # if start and end:
        st.subheader(f"General Orders Trend")
        general_time_trend(UNSTACKED_GTB)

    if "General Revenue Trend" in trends:
        st.subheader("General Revenue Trend")
        general_revenue_trend(UNSTACKED_GRB)

    if "Day / Period Heatmap Trend" in trends:
        st.subheader("Day / Period Heatmap Trend")
        day_time_heatmap_trends(UNSTACKED_DT_TREND)

    if "Day / Period Revenue Trend" in trends:
        st.subheader("Day / Period Revenue Trend")
        day_time_revenue_heatmap(UNSTACKED_DT_REVENUE)

    if "Orders Per Day Barchart" in trends:
        st.subheader("Orders Per Day Barchart")
        orders_per_day_barchart(ORDERS_PER_DAY)

    if "Seasonal Trends Barchart" in trends:
        st.subheader("Seasonal Trends Barchart")
        seasons_trends_barchart(UNSTACKED_SEASONS_TREND)

    if "Seasonal Revenue Trends" in trends:
        st.subheader("Seasonal Revenue Trends")
        seasons_revenue(UNSTACKED_REVENUE_PER_SEASON)



#
#
# start = st.date_input("Start", value=pd.to_datetime("2017-01-01"))
# end = st.date_input("End", value=pd.to_datetime("today"))
# When used:
# returned "Invalid comparison between dtype=datetime64[ns] and date"
# I don't know which one is which (see commented code inside function above)
#
#
# Working only for the DataFrame itself, can't implement the options in graphs
#
# season_tickers = ["spring", "summer", "autumn", "winter"]
# season = st.selectbox(label="Select a Season", options=season_tickers)
#
#    if season:
#
#        st.header("Dataset overview")
#        st.text("This is a nice description about the dataset")
#
#        filter_data = pd.DataFrame(data[data["order_season"] == season])
#        st.write(filter_data.head(5))
#
#        day_time_heatmap_trends(UNSTACKED_DT_TREND, season)
