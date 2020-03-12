# Add coordinates for each area in the list for the latest table sheet
# As there are limit for free account, we only call coordinates for the latest table sheet
from opencage.geocoder import OpenCageGeocode
import time
import random
import progressbar
key = 'b33700b33d0a446aa6e16c0b57fc82d1'  # get api key from:  https://opencagedata.com
geocoder = OpenCageGeocode(key)

list_lat = []   # create empty lists
list_long = []    
for index, row in dfs[keyList[0]].iterrows(): # iterate over rows in dataframe
    
    # For display progress bar
    #bar = progressbar.ProgressBar(maxval=dfs[keyList[0]].shape[0],
    #                              widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    
    City = row['Province/State']
    State = row['Country/Region']
    
    # Note that 'nan' is float
    if type(City) is str:
        if City == 'Macau' or City == 'Hong Kong':
            query = str(City)+','+'China'
            results = geocoder.geocode(query)   
            lat = results[0]['geometry']['lat']
            long = results[0]['geometry']['lng']

            list_lat.append(lat)
            list_long.append(long)
        elif City == 'Queensland':
            query = 'Brisbane'+','+str(State)
            results = geocoder.geocode(query)   
            lat = results[0]['geometry']['lat']
            long = results[0]['geometry']['lng']

            list_lat.append(lat)
            list_long.append(long)
        elif City == 'New South Wales':
            query = 'Sydney'+','+str(State)
            results = geocoder.geocode(query)   
            lat = results[0]['geometry']['lat']
            long = results[0]['geometry']['lng']

            list_lat.append(lat)
            list_long.append(long)    
        elif City == 'Victoria':
            query = 'Melbourne'+','+str(State)
            results = geocoder.geocode(query)   
            lat = results[0]['geometry']['lat']
            long = results[0]['geometry']['lng']

            list_lat.append(lat)
            list_long.append(long)
        elif City == 'South Australia':
            query = 'Adelaide'+','+str(State)
            results = geocoder.geocode(query)   
            lat = results[0]['geometry']['lat']
            long = results[0]['geometry']['lng']

            list_lat.append(lat)
            list_long.append(long)
        elif City == 'Northern Territory':
            query = 'Darwin'+','+str(State)
            results = geocoder.geocode(query)   
            lat = results[0]['geometry']['lat']
            long = results[0]['geometry']['lng']

            list_lat.append(lat)
            list_long.append(long)
        elif City == 'Western Australia':
            query = 'Perth'+','+str(State)
            results = geocoder.geocode(query)   
            lat = results[0]['geometry']['lat']
            long = results[0]['geometry']['lng']

            list_lat.append(lat)
            list_long.append(long)
        elif City == 'Tasmania':
            query = 'Hobart'+','+str(State)
            results = geocoder.geocode(query)   
            lat = results[0]['geometry']['lat']
            long = results[0]['geometry']['lng']

            list_lat.append(lat)
            list_long.append(long)
        elif City == 'From Diamond Princess cruise':
            query = 'Omaha'+','+str(State)
            results = geocoder.geocode(query)   
            lat = results[0]['geometry']['lat']
            long = results[0]['geometry']['lng']

            list_lat.append(lat)
            list_long.append(long)
        else:
            query = str(City)+','+str(State)
            results = geocoder.geocode(query)   
            lat = results[0]['geometry']['lat']
            long = results[0]['geometry']['lng']

            list_lat.append(lat)
            list_long.append(long)
            
    else:
        if State == 'Italy':
            query = 'Lombardy'+','+'Italy'
            results = geocoder.geocode(query)   
            lat = results[0]['geometry']['lat']
            long = results[0]['geometry']['lng']

            list_lat.append(lat)
            list_long.append(long)
    
        elif State == 'South Korea':
            query = 'Daegu'+','+'South Korea'
            results = geocoder.geocode(query)   
            lat = results[0]['geometry']['lat']
            long = results[0]['geometry']['lng']

            list_lat.append(lat)
            list_long.append(long)
    
        else:
            query = str(State)
            results = geocoder.geocode(query)   
            lat = results[0]['geometry']['lat']
            long = results[0]['geometry']['lng']

            list_lat.append(lat)
            list_long.append(long)
            
    # Wait a given time bewteen 1 to 15 seconds for scraping the next website to mimic a humanbeing search.
    time.sleep(random.randint(2,8))
    #bar.finish()
    print(index)
# create new columns from lists    
dfs[keyList[0]]['lat'] = list_lat   
dfs[keyList[0]]['lon'] = list_long

print('Coordinate data are generated!')