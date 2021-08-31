import geopandas as gpd
import matplotlib.pyplot as plt

##  Import counties of DE and surrounding states
counties = gpd.read_file(r'cb_2018_us_county_500k.shp')
counties = counties.to_crs(2776) ##  Chose CRS focused on DE area
counties_DE = counties[counties['STATEFP'] == '10']  ##  Three DE Counties, very merciful
DE_map = counties[counties['STATEFP'].isin(['10', '34', '42', '24'])]  ##  Area of Interest

##  Isolate each county, would create script if the sample size weren't so small
Sussex = counties_DE[counties['NAME'] == 'Sussex'].copy() ## Had to be careful, there was a Sussex, PA!
New_Castle = counties_DE[counties['NAME'] == 'New Castle'].copy()
Kent = counties_DE[counties['NAME'] == 'Kent'].copy()
#print(Kent)

##  Import all substations of DE and neighboring states
substations = gpd.read_file(r'Substations.shp')
substations = substations.to_crs(2776)
substations_total = substations[substations['STATE'].isin(['DE', 'NJ', 'PA', 'MD'])]
substations_DE = substations[substations['STATE']=='DE']
substations_DE.count()
#substation_DE_neighbors.plot()

'''
##  Side by side
fig, (ax1, ax2) = plt.subplots(ncols=2)
DE_map.plot(ax=ax1)
substations_total.plot(ax=ax2)
plt.show()
'''

##  adding 1 mile buffer to counties
Sussex['geometry'] = Sussex.geometry.buffer(1609.34)
#print(Sussex.area)
New_Castle['geometry'] = New_Castle.geometry.buffer(1609.34)
Kent['geometry']= Kent.geometry.buffer(1609.34)

##  Collapse multiple polygons to one shape
#Sussex_union = Sussex.geometry.unary_union
#New_Castle_union = New_Castle.geometry.unary_union
#Kent_union = Kent.geometry.unary_union

##  Successful join of substations within Sussex DE
sussex_substations = gpd.sjoin(substations_total, Sussex, how='inner', op='intersects')
print(sussex_substations)
sussex_substations.count()
base = DE_map.plot(color='blue', edgecolor='white')
sussex_substations.plot(ax=base, marker="*", color='orange', markersize=20)
plt.show()

##  Succesful join of substations within New Castle DE
New_Castle_substations = gpd.sjoin(substations_total, New_Castle, how='inner', op='intersects')
print(New_Castle_substations)
New_Castle_substations.count()
base = DE_map.plot(color='blue', edgecolor='white')
New_Castle_substations.plot(ax=base, marker="*", color='orange', markersize=20)
plt.show()

##  Succesful join of substations within Kent DE
Kent_substations = gpd.sjoin(substations_total, Kent, how='inner', op='intersects')
print(Kent_substations)
Kent_substations.count()
base = DE_map.plot(color='blue', edgecolor='white')
Kent_substations.plot(ax=base, marker="*", color='orange', markersize=20)
plt.show()

##  Successful join of substations within DE
#counties_with_substations = gpd.sjoin(substations_total, counties_DE, how='inner', op='intersects')
#print(counties_with_substations)
#base = DE_map.plot(color='blue', edgecolor='white')
#counties_with_substations.plot(ax=base, marker="*", color='orange', markersize=5)
#plt.show()


##  Entire Map
#base = DE_map.plot(color='blue', edgecolor='white')
#substations_total.plot(ax=base, marker="*", color='orange', markersize=20)
#plt.show()
