import pandas as pd

with open('cities_infos.txt', 'r') as f:
    # Reads the dict
    cities_infos = eval(f.read())

df_dict = {'cidade': []}
# Iterates over all cities
for city_idx, city in enumerate(cities_infos):
    city_info = cities_infos[city] # Dict with city info
    df_dict['cidade'].append(city)  # Appends city
    
    # Iterates over city's info
    for info in city_info:
        # If I did not save the info into the dict, I
        # create the key, filling the missing rows
        if info not in df_dict:
            df_dict[info] = [None] * city_idx + [city_info[info]]
        # Else, I just append
        else:
            df_dict[info].append(city_info[info])

    # This part deals with columns missing in the current city
    for key in df_dict:
        if key not in city_info and key != 'cidade':
            df_dict[key].append(None)

# Creates the DataFrame
df_cities = pd.DataFrame(df_dict)
# Saves the csv
df_cities.to_csv("cities_info.csv", index=False)