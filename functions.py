import streamlit as st
import pydeck as pdk
import pandas as pd
def heatmap():
    df = pd.read_csv('ODL_RESTAURANT.csv', sep=',', index_col=0)

    streets = []
    for street in df['street']:
        for l in street:
            if l == "-":
                head, sep, tail = street.partition('- ')
                streets.append(tail)
            else:
                streets.append(street)
                break

    from geopy.geocoders import Nominatim
    locator = Nominatim(user_agent="myGeocoder")
    lat = []
    cities = []
    lon = []
    new_street = []

    for street in streets:
        if locator.geocode(f"{street} SF", timeout=10000) != None:
            cities.append("San Francisco")
            new_street.append(street)
            location = locator.geocode(f"{street} SF", timeout=10000)
            lat.append(location.latitude)
            lon.append(location.longitude)

        elif locator.geocode(f"{street} NYC", timeout=10000) != None:
            cities.append('New York')
            new_street.append(street)
            location = locator.geocode(f"{street} NYC", timeout=10000)
            lat.append(location.latitude)
            lon.append(location.longitude)

    count = 0
    freq = []
    mg = pd.read_csv('full_table_v0.3.csv', sep=',', index_col=0)
    for street in new_street:
        for streat in mg['street']:
            if street == streat:
                count += 1

        freq.append(count)
        count = 0

    heat_map = pd.DataFrame({'lat': lat, 'lon': lon, 'street_names': new_street, 'count': freq, 'cities': cities})
    heat_map = heat_map.sort_values(by='cities', ascending=True)
    city = heat_map['cities'].tolist()
    rep = heat_map['count'].tolist()
    ind = 0

    for i in city:
        ind += 1
        if i != 'New York':
            ind -= 1
            break

    ny_lat = []
    ny_lon = []
    sf_lat = []
    sf_lon = []
    i = 0
    for count in rep:
        if freq.index(count) >= ind:
            for n in range(0, count):
                sf_lat.append(lat[i])
                sf_lon.append(lon[i])
        else:
            for n in range(0, count):
                ny_lat.append(lat[i])
                ny_lon.append(lon[i])
        i += 1

    ny_df=pd.DataFrame({'lat': ny_lat, 'lon':ny_lon})
    sf_df=pd.DataFrame({'lat': sf_lat, 'lon':sf_lon})


    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=37.76,
            longitude=-122.4,
            zoom=11,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                'HexagonLayer',
                data=ny_df,
                get_position='[lon, lat]',
                radius=200,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
            pdk.Layer(
                'ScatterplotLayer',
                data=ny_df,
                get_position='[lon, lat]',
                get_color='[200, 30, 0, 160]',
                get_radius=200,
            ),
        ],
    ))

    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=37.76,
            longitude=-122.4,
            zoom=11,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                'HexagonLayer',
                data=sf_df,
                get_position='[lon, lat]',
                radius=200,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
            pdk.Layer(
                'ScatterplotLayer',
                data=sf_df,
                get_position='[lon, lat]',
                get_color='[200, 30, 0, 160]',
                get_radius=200,
            ),
        ],
    ))




def revenue_cent():
    df = pd.read_csv('full_table_v0.3.csv', sep=',', index_col=0)
    delivery = df.groupby(["rest_name"], as_index=False)["revenue"].value_counts().sort_values(by="revenue",
                                                                                               ascending=True)
    delivery['rest_rev'] = delivery['revenue'].astype(float)*delivery['count'].astype(float)
    total_rev = delivery.groupby(['rest_name']).sum().sort_values(by='count', ascending=True)
    rev_sum = df.revenue.sum()

    percent=[]
    for i in total_rev['rest_rev']:
        percent.append((i / float(rev_sum)) * 100)

    total_rev['percent'] = percent

    return total_rev

def not_selling():
    df = pd.read_csv('full_table_v0.3.csv', sep=',', index_col=0)
    table = df.groupby(["rest_name"], as_index=False)["revenue"].value_counts().sort_values(by="revenue",
                                                                                            ascending=True)
    table['rest_rev'] = table['revenue'].astype(float) * table['count'].astype(float)
    table = table.sort_values(['rest_name', 'count'], ascending=True)
    name_list = table['rest_name']
    i = 1
    indexes = []
    for name in name_list:
        if name != name_list[i]:
            if name_list[i]==name_list[i+1]:
                indexes.append(i)
        i += 1
        if i == 8126:
            break

    table = table.reset_index()
    del table['index']
    table = table.drop(indexes)
    table = table.drop(0)
    fin_table = table.groupby(['rest_name']).sum().sort_values(by='count', ascending=True)
    rev_sum = df.revenue.sum()
    percent = []
    for i in fin_table['rest_rev']:
        percent.append((i / float(rev_sum)) * 100)

    fin_table['percent'] = percent

    old_table = revenue_cent()
    fin_table['diff']=old_table['percent']-fin_table['percent']
    fin_table['old_percent']=old_table['percent']


def get_zipcode(geolocator, lat_field, lon_field):
    location = geolocator.reverse((lat_field, lon_field))
    return location.raw['address']['postcode']


