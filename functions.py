def heatmap():
    df = pd.read_csv('ODL_RESTAURANT.csv', sep=',', index_col=0)

    from geopy.geocoders import Nominatim
    locator = Nominatim(user_agent="myGeocoder")
    lat = []
    streets = []
    cities = []
    lon = []
    zip=[]
    for street in df['street']:
        if locator.geocode(f"{street} SF", timeout=10000) != None:
            cities.append("San Francisco")
            location = locator.geocode(f"{street} SF", timeout=10000)
            lat.append(location.latitude)
            lon.append(location.longitude)
            zip.append(get_zipcode(location.latitude,location.longitude))
            streets.append(street)

        elif locator.geocode(f"{street} NYC", timeout=10000) != None:
            cities.append('New York')
            location = locator.geocode(f"{street} NYC", timeout=10000)
            lat.append(location.latitude)
            lon.append(location.longitude)
            zip.append(get_zipcode(location.latitude,location.longitude))
            streets.append(street)

    count = 0
    freq = []
    mg=pd.read_csv('full_table_v0.3.csv', sep=',', index_col=0)
    for street in streets:
        for streat in mg['street']:
            if street == streat:
                count += 1

        freq.append(count)
        count = 0

    heat_map = pd.DataFrame({'lat': lat, 'lon':lon, 'street_names': streets, 'count': freq, 'cities':cities}, 'zip':zip)
    heat_map = heat_map.sort_values(by='cities', ascending=True)

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


